import platform
import shutil
from dataclasses import dataclass
from pathlib import Path

import PyInstaller.__main__


@dataclass(frozen=True)
class BuildArtifacts:
    zip_path: Path
    bin_path: Path


def test_pyinstaller(project_root: Path) -> None:
    artifacts = build(project_root)
    assert artifacts.bin_path.is_file()
    assert artifacts.zip_path.is_file()


def build(project_root: Path) -> BuildArtifacts:
    plat = platform.system().lower()
    name = f"zero_{plat}"
    binary_name = f"{name}.exe" if plat == "windows" else name

    PyInstaller.__main__.run(
        [
            "src/zero/__main__.py",
            "--noconfirm",
            "--onedir",
            "--windowed",
            "--name",
            name,
        ],
    )
    dist_name = project_root / Path(f"dist/{name}")
    artifacts_root_dir = dist_name
    dist_dir = project_root / Path("dist")
    zip_file = Path(f"{name}.zip")
    dist_zip = dist_dir / zip_file
    shutil.make_archive(name, "zip", artifacts_root_dir)
    shutil.rmtree(artifacts_root_dir)
    shutil.move(zip_file, dist_zip)

    PyInstaller.__main__.run(
        [
            "src/zero/__main__.py",
            "--noconfirm",
            "--onefile",
            "--windowed",
            "--name",
            binary_name,
        ],
    )
    dist_binary = dist_dir / binary_name
    return BuildArtifacts(dist_zip, dist_binary)
