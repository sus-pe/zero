import logging
import shutil
import subprocess
import sys
from pathlib import Path

logger = logging.getLogger(__name__)


def exit_if_no_cargo() -> Path:
    cargo = shutil.which("cargo")
    if not cargo:
        logger.error(
            "cargo not installed. Please install Rust from https://rustup.rs/!"
        )
        sys.exit(1)

    logger.info("Found cargo: %s", cargo)
    return Path(cargo).resolve()


def install_taplo(cargo: Path) -> None:
    if not shutil.which("taplo"):
        logger.info("Executing cargo from path: %s", cargo)
        # ruff: noqa: S603 (Allow passing cargo command as parameter).
        result = subprocess.run(
            [cargo, "install", "taplo-cli"],
            check=False,  # let us inspect returncode instead of raising
        )

        if result.returncode == 0:
            logger.info("✅ Taplo installed successfully.")
        else:
            logger.error(
                "❌ Failed to execute `cargo install taplo-cli`, please debug. "
            )
            sys.exit(result.returncode)


if __name__ == "__main__":
    cargo_path = exit_if_no_cargo()
    install_taplo(cargo_path)
