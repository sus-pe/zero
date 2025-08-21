import platform
import shutil
from dataclasses import dataclass
from pathlib import Path
from subprocess import run

import PyInstaller.__main__
import pytest


@dataclass(frozen=True)
class BuildArtifacts:
    zip_path: Path
    bin_path: Path


@pytest.mark.slow
def test_pyinstaller(project_root: Path) -> None:
    artifacts = build(project_root)
    assert artifacts.bin_path.is_file()
    assert artifacts.zip_path.is_file()
    # ruff: noqa: S603
    run([artifacts.bin_path, "--send-quit"], check=True)


def build(project_root: Path) -> BuildArtifacts:
    dist_dir = project_root / Path("dist")
    plat = platform.system().lower()
    name = f"zero_{plat}"
    binary_name = f"{name}.exe" if plat == "windows" else name

    pyinstaller(name)
    dist_name = project_root / Path(f"dist/{name}")
    artifacts_root_dir = dist_name
    zip_file = Path(f"{name}.zip")
    dist_zip = dist_dir / zip_file
    shutil.make_archive(name, "zip", artifacts_root_dir)
    shutil.rmtree(artifacts_root_dir)
    shutil.move(zip_file, dist_zip)
    pyinstaller(binary_name, one_file=True)
    dist_binary = dist_dir / binary_name
    return BuildArtifacts(dist_zip, dist_binary)


def pyinstaller(name: str, *, one_file: bool = False) -> None:
    args: list[str] = [
        "--collect-data",
        "zero",
        "--noconfirm",
        "--windowed",
        "--name",
        name,
        "src/zero/__main__.py",
    ]
    if one_file:
        args.append("--onefile")
    PyInstaller.__main__.run(args)
