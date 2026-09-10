"""Protect verified, repeatable installation without network dependencies."""

import hashlib
import io
import tarfile
import zipfile
from dataclasses import asdict, replace
from pathlib import Path

import pytest

from scripts.bootstrap_tools import Release, install, parse_release, select_platform

EXECUTABLE_BITS = 0o111


@pytest.fixture
def release() -> Release:
    return Release(
        "example",
        "1.0",
        "linux_x86_64",
        "https://example.invalid/tool",
        "0" * 64,
        "example",
        "binary",
    )


def cache_release(directory: Path, release: Release, payload: bytes) -> Release:
    cache = directory / "downloads"
    cache.mkdir(parents=True)
    (cache / f"{release.name}-{release.version}-{release.platform}").write_bytes(payload)
    return replace(release, sha256=hashlib.sha256(payload).hexdigest())


@pytest.mark.parametrize("archive_format", ["binary", "zip", "tar"])
def test_verified_cached_install_is_repeatable(
    tmp_path: Path,
    release: Release,
    archive_format: str,
) -> None:
    executable = b"synthetic test executable"
    buffer = io.BytesIO()
    if archive_format == "zip":
        with zipfile.ZipFile(buffer, "w") as archive:
            archive.writestr("example", executable)
            archive.writestr("../../unrelated", b"must never be extracted")
    elif archive_format == "tar":
        with tarfile.open(fileobj=buffer, mode="w") as archive:
            member = tarfile.TarInfo("example")
            member.size = len(executable)
            archive.addfile(member, io.BytesIO(executable))
    else:
        buffer.write(executable)
    selected = cache_release(tmp_path, replace(release, archive=archive_format), buffer.getvalue())
    install(selected, tmp_path)
    install(selected, tmp_path)
    binary = tmp_path / "bin" / "example"
    assert binary.read_bytes() == executable
    assert binary.stat().st_mode & EXECUTABLE_BITS == EXECUTABLE_BITS
    assert set(tmp_path.iterdir()) == {tmp_path / "bin", tmp_path / "downloads"}


def test_checksum_failure_preserves_installed_binary(tmp_path: Path, release: Release) -> None:
    selected = cache_release(tmp_path, release, b"verified executable")
    install(selected, tmp_path)
    cached = next((tmp_path / "downloads").iterdir())
    cached.write_bytes(b"corrupt replacement")
    with pytest.raises(ValueError, match="Checksum mismatch"):
        install(selected, tmp_path)
    assert (tmp_path / "bin" / "example").read_bytes() == b"verified executable"
    assert cached.read_bytes() == b"corrupt replacement"


@pytest.mark.parametrize("member", ["../escape", "/absolute", "folder/../../escape", "a\\b"])
def test_manifest_rejects_unsafe_members(release: Release, member: str) -> None:
    with pytest.raises(ValueError, match="Unsafe archive member"):
        parse_release(asdict(replace(release, member=member)))


def test_tar_link_is_not_installed(tmp_path: Path, release: Release) -> None:
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w") as archive:
        member = tarfile.TarInfo("example")
        member.type = tarfile.SYMTYPE
        member.linkname = "/outside"
        archive.addfile(member)
    selected = cache_release(tmp_path, replace(release, archive="tar"), buffer.getvalue())
    with pytest.raises(ValueError, match="Invalid executable member"):
        install(selected, tmp_path)
    assert not (tmp_path / "bin").exists()


@pytest.mark.parametrize("case", ["missing", "duplicate", "unsupported"])
def test_incomplete_platform_is_rejected(release: Release, case: str) -> None:
    other = replace(release, name="another", platform="darwin_arm64")
    records = [release, other] if case == "missing" else [release, release]
    host = "unknown" if case == "unsupported" else release.platform
    with pytest.raises(ValueError, match="Unsupported or incomplete"):
        select_platform(records, host)


def test_complete_platform_selects_each_tool_once(release: Release) -> None:
    second = replace(release, name="another")
    other_host = replace(release, platform="darwin_arm64")
    assert select_platform([release, second, other_host], release.platform) == [release, second]
