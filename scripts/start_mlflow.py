"""Launch local MLflow using mounted runtime credentials."""

import json
import os
import socket
from pathlib import Path

import psycopg
from mlflow.cli import server


def main() -> None:
    """Create a separate tracking database and start the real tracking service."""
    password = Path("/run/secrets/postgres_password").read_text(encoding="utf-8")
    with psycopg.connect(
        host="postgres", user="postgres", password=password, autocommit=True
    ) as connection:
        exists = connection.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s", ("mlflow",)
        ).fetchone()
        if exists is None:
            connection.execute("CREATE DATABASE mlflow")
    config = json.loads(Path("/run/secrets/s3_config").read_text(encoding="utf-8"))
    credentials = config["identities"][0]["credentials"][0]
    os.environ["AWS_ACCESS_KEY_ID"] = credentials["accessKey"]
    os.environ["AWS_SECRET_ACCESS_KEY"] = credentials["secretKey"]
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-1"
    os.environ["MLFLOW_S3_ENDPOINT_URL"] = "http://object-store:8333"
    os.environ["MLFLOW_BACKEND_STORE_URI"] = (
        f"postgresql+psycopg://postgres:{password}@postgres/mlflow"
    )
    server.main(
        [
            "--host",
            socket.gethostbyname(socket.gethostname()),
            "--allowed-hosts",
            "mlflow:5000,localhost:5000",
            "--artifacts-destination",
            "s3://mlflow-artifacts",
        ],
    )


if __name__ == "__main__":
    main()
