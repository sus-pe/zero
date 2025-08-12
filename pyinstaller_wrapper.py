import platform
import shutil

import PyInstaller.__main__

plat = platform.system().lower()

name = f"zero_{plat}"

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
shutil.make_archive(name, "zip", f"dist/{name}")
shutil.rmtree(f"dist/{name}")
shutil.move(f"{name}.zip", f"dist/{name}.zip")

PyInstaller.__main__.run(
    [
        "src/zero/__main__.py",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--name",
        name,
    ],
)
