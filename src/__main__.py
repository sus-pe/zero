"""
Provides an entrypoint for running as wheel, e.g. `python zero*.whl`
"""

import typer

from zero.__main__ import main

if __name__ == "__main__":  # pragma: no cover
    typer.run(main)
