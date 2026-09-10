"""Behavioral rules for rendered Compose configuration."""

from copy import deepcopy

import pytest

from verification.compose_policy import check_compose


@pytest.fixture
def safe_compose() -> dict[str, object]:
    """Represent external, locally built and local consumer services."""
    return {
        "services": {
            "database": {
                "image": "postgres:17@sha256:" + "a" * 64,
                "networks": ["foundation"],
            },
            "builder": {
                "image": "podium-foundation:local",
                "build": {"context": "/workspace"},
                "networks": ["foundation"],
                "ports": [{"target": 5000, "published": "5000", "host_ip": "127.0.0.1"}],
                "volumes": [{"type": "volume", "target": "/cache"}],
            },
            "consumer": {
                "image": "podium-foundation:local",
                "networks": {"foundation": {}},
            },
        },
        "networks": {"foundation": {"internal": True}},
    }


def test_safe_rendered_compose_passes(safe_compose: dict[str, object]) -> None:
    assert not check_compose(safe_compose)


@pytest.mark.parametrize(
    ("change", "rule"),
    [
        ({"privileged": True}, "COMPOSE002"),
        ({"network_mode": "host"}, "COMPOSE002"),
        (
            {
                "volumes": [
                    {
                        "type": "bind",
                        "source": "/Users/example/.orbstack/run/docker.sock",
                        "target": "/var/run/docker.sock",
                    }
                ]
            },
            "COMPOSE002",
        ),
        ({"image": "postgres:latest"}, "COMPOSE003"),
        ({"ports": [{"target": 5432, "published": "5432"}]}, "COMPOSE001"),
        (
            {"ports": [{"target": 5432, "published": 5432, "host_ip": "192.0.2.1"}]},
            "COMPOSE004",
        ),
        ({"networks": ["public"]}, "COMPOSE005"),
    ],
)
def test_unsafe_service_capabilities_fail(
    safe_compose: dict[str, object], change: dict[str, object], rule: str
) -> None:
    document = deepcopy(safe_compose)
    services = document["services"]
    assert isinstance(services, dict)
    database = services["database"]
    assert isinstance(database, dict)
    database.update(change)
    assert rule in {finding.rule for finding in check_compose(document)}


@pytest.mark.parametrize(
    "document",
    [
        [],
        {},
        {"services": [], "networks": {}},
        {"services": {"database": []}, "networks": {"foundation": {"internal": True}}},
        {
            "services": {"database": {"image": 42, "networks": ["foundation"]}},
            "networks": {"foundation": {"internal": True}},
        },
        {
            "services": {"database": {"image": "postgres@sha256:" + "a" * 64}},
            "networks": {"foundation": {"internal": True}},
        },
        {
            "services": {
                "database": {
                    "image": "local:latest",
                    "build": None,
                    "networks": ["foundation"],
                }
            },
            "networks": {"foundation": {"internal": True}},
        },
        {
            "services": {
                "builder": {
                    "image": "mutable-builder:latest",
                    "build": {"context": "https://example.invalid/repository.git"},
                    "networks": ["foundation"],
                }
            },
            "networks": {"foundation": {"internal": True}},
        },
        {
            "services": {
                "database": {
                    "image": "postgres@sha256:" + "a" * 64,
                    "volumes": [{"source": [], "target": "/var/lib/postgresql/data"}],
                    "networks": ["foundation"],
                }
            },
            "networks": {"foundation": {"internal": True}},
        },
    ],
)
def test_missing_or_malformed_required_shapes_fail(document: object) -> None:
    assert "COMPOSE001" in {finding.rule for finding in check_compose(document)}
