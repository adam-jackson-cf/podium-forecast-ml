"""Validate rendered Compose JSON without starting services."""

import json
import re
import sys
from collections.abc import Iterable, Mapping
from ipaddress import ip_address
from pathlib import PurePosixPath

from verification.findings import Finding

DIGESTED_IMAGE = re.compile(r"^\S+@sha256:[0-9a-f]{64}$")


def check_compose(document: object) -> list[Finding]:
    """Fail closed on malformed shapes and unsafe service capabilities."""
    findings: list[Finding] = []
    if not isinstance(document, dict):
        return [_finding("COMPOSE001", "Rendered Compose input must be an object.")]
    services = document.get("services")
    networks = document.get("networks")
    if not isinstance(services, dict) or not services:
        findings.append(
            _finding("COMPOSE001", "Rendered Compose services must be a non-empty object.")
        )
        return findings
    if not isinstance(networks, dict) or not networks:
        findings.append(
            _finding("COMPOSE001", "Rendered Compose networks must be a non-empty object.")
        )
        return findings

    local_images = {
        service["image"]
        for service in services.values()
        if isinstance(service, dict)
        and _valid_build(service.get("build"))
        and isinstance(service.get("image"), str)
    }
    for service_name, service in services.items():
        if not isinstance(service_name, str) or not isinstance(service, dict):
            findings.append(
                _finding("COMPOSE001", "Every rendered Compose service must be an object.")
            )
            continue
        findings.extend(_check_service(service_name, service, networks, local_images))
    return findings


def _check_service(
    name: str,
    service: Mapping[str, object],
    networks: Mapping[str, object],
    local_images: set[object],
) -> Iterable[Finding]:
    if service.get("privileged") is True:
        yield _service_finding(name, "COMPOSE002", "privileged execution is forbidden.")
    if service.get("network_mode") == "host":
        yield _service_finding(name, "COMPOSE002", "host network mode is forbidden.")
    if "privileged" in service and not isinstance(service["privileged"], bool):
        yield _service_finding(name, "COMPOSE001", "privileged must be a boolean.")

    image = service.get("image")
    has_build = "build" in service
    if has_build and not _valid_build(service.get("build")):
        yield _service_finding(name, "COMPOSE001", "build must contain a non-empty context.")
    if image is None and not has_build:
        yield _service_finding(name, "COMPOSE001", "an image or build definition is required.")
    elif image is not None and not isinstance(image, str):
        yield _service_finding(name, "COMPOSE001", "image must be a string.")
    elif (
        isinstance(image, str) and image not in local_images and not DIGESTED_IMAGE.fullmatch(image)
    ):
        yield _service_finding(name, "COMPOSE003", "external images must use a sha256 digest.")

    yield from _check_volumes(name, service.get("volumes", []))
    yield from _check_ports(name, service.get("ports", []))
    yield from _check_networks(name, service.get("networks"), networks)


def _check_volumes(name: str, volumes: object) -> Iterable[Finding]:
    if not isinstance(volumes, list):
        yield _service_finding(name, "COMPOSE001", "volumes must be a list.")
        return
    for volume in volumes:
        if not isinstance(volume, dict):
            yield _service_finding(name, "COMPOSE001", "volume entries must be objects.")
            continue
        source = volume.get("source")
        target = volume.get("target")
        if not isinstance(target, str) or (source is not None and not isinstance(source, str)):
            yield _service_finding(
                name, "COMPOSE001", "volume target and any source must be strings."
            )
            continue
        if (isinstance(source, str) and _is_docker_socket(source)) or _is_docker_socket(target):
            yield _service_finding(name, "COMPOSE002", "direct Docker socket mounts are forbidden.")


def _check_ports(name: str, ports: object) -> Iterable[Finding]:
    if not isinstance(ports, list):
        yield _service_finding(name, "COMPOSE001", "ports must be a list.")
        return
    for port in ports:
        if not isinstance(port, dict):
            yield _service_finding(name, "COMPOSE001", "port entries must be objects.")
            continue
        host_ip = port.get("host_ip")
        if not isinstance(host_ip, str):
            yield _service_finding(name, "COMPOSE001", "published ports require a host_ip string.")
            continue
        if not _is_loopback(host_ip):
            yield _service_finding(name, "COMPOSE004", "published ports must bind to loopback.")


def _valid_build(build: object) -> bool:
    if not isinstance(build, dict):
        return False
    context = build.get("context")
    return isinstance(context, str) and PurePosixPath(context).is_absolute()


def _is_docker_socket(path: str) -> bool:
    return PurePosixPath(path).name == "docker.sock"


def _is_loopback(host_ip: str) -> bool:
    try:
        return ip_address(host_ip).is_loopback
    except ValueError:
        return False


def _check_networks(
    name: str, service_networks: object, declared_networks: Mapping[str, object]
) -> Iterable[Finding]:
    if isinstance(service_networks, list):
        references = service_networks
    elif isinstance(service_networks, dict):
        references = list(service_networks)
    else:
        yield _service_finding(name, "COMPOSE001", "networks must be a list or object.")
        return
    if not references or not all(isinstance(reference, str) for reference in references):
        yield _service_finding(name, "COMPOSE001", "at least one named network is required.")
        return
    for reference in references:
        network = declared_networks.get(reference)
        if not isinstance(network, dict) or network.get("internal") is not True:
            yield _service_finding(
                name, "COMPOSE005", "services must use declared internal networks."
            )


def _finding(rule: str, message: str) -> Finding:
    return Finding("compose", 1, rule, message)


def _service_finding(name: str, rule: str, message: str) -> Finding:
    return _finding(rule, f"Service {name!r}: {message}")


def main() -> int:
    """Read rendered JSON from stdin and emit sanitized policy diagnostics."""
    try:
        document = json.load(sys.stdin)
    except (json.JSONDecodeError, UnicodeError):
        sys.stderr.write("compose:1: COMPOSE001 Rendered Compose input is not valid JSON.\n")
        return 1
    findings = check_compose(document)
    for finding in findings:
        sys.stderr.write(f"{finding.render()}\n")
    if findings:
        return 1
    sys.stdout.write("Compose policy: rendered configuration passed.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
