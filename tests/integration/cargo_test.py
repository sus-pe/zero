import shutil


def test_cargo_and_taplo_installed() -> None:
    assert shutil.which("cargo"), (
        "cargo not installed. Please install Rust from https://rustup.rs/!"
    )
    assert shutil.which("taplo"), "taplo-cli not installed. Please install via cargo!"
