"""One real foundation journey; test fixtures are not production ML behaviour."""

import hashlib
import json
from pathlib import Path
from uuid import uuid4

import boto3
import psycopg
import pyarrow as pa
import pyarrow.parquet as pq
import pytest
from botocore.config import Config
from mlflow import MlflowClient
from mypy_boto3_s3 import S3Client
from psycopg import sql


def object_client() -> S3Client:
    """Connect to the real local S3 primitive using mounted credentials."""
    config = json.loads(Path("/run/secrets/s3_config").read_text(encoding="utf-8"))
    credentials = config["identities"][0]["credentials"][0]
    return boto3.client(
        "s3",
        endpoint_url="http://object-store:8333",
        region_name="eu-west-1",
        aws_access_key_id=credentials["accessKey"],
        aws_secret_access_key=credentials["secretKey"],
        config=Config(s3={"addressing_style": "path"}),
    )


def extract_fixture() -> list[tuple[int, int, float]]:
    """Prove extraction works and writes fail under a real restricted role."""
    password = Path("/run/secrets/postgres_password").read_text(encoding="utf-8")
    role = "extract_" + uuid4().hex
    with psycopg.connect(host="postgres", user="postgres", password=password) as db:
        db.execute("CREATE TABLE race_fixture (race_id INT, runner_id INT, price FLOAT)")
        db.execute("INSERT INTO race_fixture VALUES (1, 1, 2.0), (1, 2, 3.0)")
        db.execute(
            sql.SQL("CREATE ROLE {} LOGIN PASSWORD {}").format(
                sql.Identifier(role), sql.Literal(password)
            )
        )
        db.execute(sql.SQL("GRANT SELECT ON race_fixture TO {}").format(sql.Identifier(role)))
    with psycopg.connect(
        host="postgres", user=role, password=password, dbname="postgres", autocommit=True
    ) as reader:
        rows = reader.execute(
            "SELECT race_id, runner_id, price FROM race_fixture ORDER BY runner_id"
        ).fetchall()
        with pytest.raises(psycopg.errors.InsufficientPrivilege):
            reader.execute("INSERT INTO race_fixture VALUES (2, 3, 4.0)")
    return [(int(row[0]), int(row[1]), float(row[2])) for row in rows]


def test_foundation_journey(tmp_path: Path) -> None:
    """Extract, version Parquet and retrieve identical tracked artifact bytes."""
    rows = extract_fixture()
    assert rows == [(1, 1, 2.0), (1, 2, 3.0)]
    table = pa.table(
        {
            "race_id": [row[0] for row in rows],
            "runner_id": [row[1] for row in rows],
            "price": [row[2] for row in rows],
        }
    )
    dataset = tmp_path / "dataset.parquet"
    pq.write_table(table, dataset)
    payload = dataset.read_bytes()
    storage = object_client()
    storage.create_bucket(Bucket="datasets")
    storage.create_bucket(Bucket="mlflow-artifacts")
    storage.put_bucket_versioning(Bucket="datasets", VersioningConfiguration={"Status": "Enabled"})
    first = storage.put_object(Bucket="datasets", Key="fixture.parquet", Body=payload)
    storage.put_object(Bucket="datasets", Key="fixture.parquet", Body=b"new revision")
    restored = storage.get_object(
        Bucket="datasets", Key="fixture.parquet", VersionId=first["VersionId"]
    )
    assert restored["Body"].read() == payload
    assert pq.read_table(dataset).to_pylist() == table.to_pylist()
    tracking = MlflowClient(tracking_uri="http://mlflow:5000")
    experiment = tracking.create_experiment("foundation-" + uuid4().hex)
    run = tracking.create_run(experiment)
    tracking.log_param(run.info.run_id, "dataset_sha256", hashlib.sha256(payload).hexdigest())
    tracking.log_artifact(run.info.run_id, str(dataset))
    downloaded = tracking.download_artifacts(
        run.info.run_id, "dataset.parquet", str(tmp_path / "download")
    )
    assert Path(downloaded).read_bytes() == payload
    tracking.set_terminated(run.info.run_id)
    persisted = tracking.get_run(run.info.run_id)
    assert persisted.info.status == "FINISHED"
    assert persisted.data.params["dataset_sha256"] == hashlib.sha256(payload).hexdigest()
