"""
Provides an entrypoint for running as wheel, e.g. `python zero*.whl`
"""

import typer

from zero.__main__ import _cli_main

if __name__ == "__main__":  # pragma: no cover
    typer.run(_cli_main)
