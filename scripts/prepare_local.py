"""Create private, ephemeral development credentials without displaying them."""

import json
import os
import secrets
from pathlib import Path


def main() -> None:
    """Write credentials consumed by Docker Compose secret mounts."""
    directory = Path(os.environ.get("LOCAL_SECRETS_DIR", ".local-runtime"))
    directory.mkdir(mode=0o700, exist_ok=True)
    password_path = directory / "postgres_password"
    config_path = directory / "s3_config.json"
    if password_path.exists() or config_path.exists():
        raise FileExistsError("Local credentials already exist; retain or remove explicitly")
    password_path.write_text(secrets.token_urlsafe(32), encoding="utf-8")
    config = {
        "identities": [
            {
                "name": "local-foundation",
                "credentials": [
                    {"accessKey": secrets.token_hex(16), "secretKey": secrets.token_hex(32)}
                ],
                "actions": ["Admin", "Read", "Write", "List", "Tagging"],
            }
        ]
    }
    config_path.write_text(json.dumps(config), encoding="utf-8")
    password_path.chmod(0o644)
    config_path.chmod(0o644)


if __name__ == "__main__":
    main()
