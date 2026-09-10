"""Install the checksum-pinned verification toolchain without executing downloads."""

from __future__ import annotations

import hashlib
import http.client
import json
import platform
import re
import stat
import tarfile
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit

MAX_BYTES = 256 * 1024 * 1024
MAX_REDIRECTS = 5


@dataclass(frozen=True)
class Release:
    name: str
    version: str
    platform: str
    url: str
    sha256: str
    member: str
    archive: str


def parse_release(record: object) -> Release:
    """Reject malformed manifest entries before accessing the filesystem."""
    fields = set(Release.__dataclass_fields__)
    if not isinstance(record, dict) or set(record) != fields:
        raise ValueError("Unexpected release manifest fields")
    if not all(isinstance(value, str) for value in record.values()):
        raise ValueError("Release fields must be strings")
    release = Release(**record)
    if not re.fullmatch(r"[a-z]+", release.name):
        raise ValueError("Invalid executable name")
    if not re.fullmatch(r"[a-zA-Z0-9_.-]+", release.version + release.platform):
        raise ValueError("Invalid version or platform")
    if not re.fullmatch(r"[0-9a-f]{64}", release.sha256):
        raise ValueError("Invalid SHA256")
    member = PurePosixPath(release.member)
    if member.is_absolute() or ".." in member.parts or "\\" in release.member:
        raise ValueError("Unsafe archive member")
    if release.archive not in {"zip", "tar", "binary"}:
        raise ValueError("Unsupported archive format")
    return release


def download(url: str, redirects: int = 0) -> bytes:
    """Fetch HTTPS artifacts with bounded payload size and socket timeout."""
    location = urlsplit(url)
    if location.scheme != "https" or not location.hostname or location.username:
        raise ValueError("Downloads require an HTTPS URL without credentials")
    if redirects > MAX_REDIRECTS:
        raise ValueError("Too many download redirects")
    connection = http.client.HTTPSConnection(location.hostname, timeout=30)
    try:
        target = location.path + ("?" + location.query if location.query else "")
        connection.request("GET", target, headers={"User-Agent": "podium-tool-bootstrap"})
        response = connection.getresponse()
        if response.status in {301, 302, 303, 307, 308}:
            return download(response.getheader("Location", ""), redirects + 1)
        if response.status != http.client.OK:
            raise RuntimeError(f"Tool download failed: HTTP {response.status}")
        payload = response.read(MAX_BYTES + 1)
        if len(payload) > MAX_BYTES:
            raise ValueError("Tool download exceeds size limit")
        return payload
    finally:
        connection.close()


def verified_archive(release: Release, cache: Path) -> Path:
    """Revalidate cached artifacts; never replace a corrupt cache silently."""
    cache.mkdir(parents=True, exist_ok=True)
    destination = cache / f"{release.name}-{release.version}-{release.platform}"
    if destination.exists() and destination.stat().st_size > MAX_BYTES:
        raise ValueError("Cached artifact exceeds size limit")
    payload = destination.read_bytes() if destination.exists() else download(release.url)
    if hashlib.sha256(payload).hexdigest() != release.sha256:
        raise ValueError(f"Checksum mismatch for {release.name}")
    if not destination.exists():
        destination.write_bytes(payload)
    return destination


def read_executable(archive: Path, release: Release) -> bytes:
    """Read exactly the declared regular file; never extract archive paths."""
    if release.archive == "binary":
        return archive.read_bytes()
    if release.archive == "zip":
        with zipfile.ZipFile(archive) as bundle:
            entry = bundle.getinfo(release.member)
            mode = entry.external_attr >> 16
            if entry.is_dir() or stat.S_ISLNK(mode) or entry.file_size > MAX_BYTES:
                raise ValueError("Invalid executable member")
            return bundle.read(entry)
    with tarfile.open(archive) as bundle:
        member = bundle.getmember(release.member)
        if not member.isfile() or member.size > MAX_BYTES:
            raise ValueError("Invalid executable member")
        stream = bundle.extractfile(member)
        if stream is None:
            raise ValueError("Missing executable member")
        with stream:
            return stream.read(MAX_BYTES + 1)


def install(release: Release, directory: Path) -> None:
    archive = verified_archive(release, directory / "downloads")
    payload = read_executable(archive, release)
    binary = directory / "bin" / release.name
    binary.parent.mkdir(parents=True, exist_ok=True)
    temporary = binary.with_suffix(".installing")
    temporary.write_bytes(payload)
    temporary.chmod(0o755)
    temporary.replace(binary)


def select_platform(releases: list[Release], host: str) -> list[Release]:
    """Require complete, unique tool coverage for the selected platform."""
    expected = {release.name for release in releases}
    selected = [release for release in releases if release.platform == host]
    names = {release.name for release in selected}
    if not selected or names != expected or len(names) != len(selected):
        raise ValueError(f"Unsupported or incomplete toolchain platform: {host}")
    return selected


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    host = f"{platform.system().lower()}_{platform.machine().lower()}"
    records = json.loads((root / "tools.lock.json").read_text())
    releases = [parse_release(record) for record in records]
    for release in select_platform(releases, host):
        install(release, root / ".tools")


if __name__ == "__main__":
    main()
