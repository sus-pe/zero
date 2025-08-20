import shutil


def test_cargo_installed() -> None:
    assert shutil.which("cargo"), (
        "cargo not installed. Please install Rust from https://rustup.rs/!"
    )


def test_taplo_installed() -> None:
    assert shutil.which("taplo"), "taplo-cli not installed. Please install via cargo!"
