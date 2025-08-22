from pathlib import Path
from sys import platform

CURRENT_OS = platform.lower()
ONEDIR_ARTIFACT_NAME = f"zero_{CURRENT_OS}"
ONEFILE_ARTIFACT_NAME = f"{ONEDIR_ARTIFACT_NAME}.bin"
ONEFILE_ARTIFACT_EXECUTABLE_NAME = (
    f"{ONEFILE_ARTIFACT_NAME}.exe" if CURRENT_OS == "win32" else (ONEDIR_ARTIFACT_NAME)
)
MAIN_SCRIPT = Path(__file__).resolve().parent.joinpath("__main__.py")
DIST_NAME = Path("dist")
ONEDIR_DIST_ARTIFACT = DIST_NAME / ONEDIR_ARTIFACT_NAME
