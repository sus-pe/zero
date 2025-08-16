import logging
import shutil
import sys

logger = logging.getLogger(__name__)


def exit_if_no_cargo() -> None:
    cargo = shutil.which("cargo")
    if not cargo:
        logger.error(
            "cargo not installed. Please install Rust from https://rustup.rs/!"
        )
        sys.exit(1)


def exit_if_no_taplo() -> None:
    if not shutil.which("taplo"):
        logger.error("taplo-cli not installed. Please install via cargo!")
        sys.exit(1)


if __name__ == "__main__":
    exit_if_no_cargo()
    exit_if_no_taplo()
