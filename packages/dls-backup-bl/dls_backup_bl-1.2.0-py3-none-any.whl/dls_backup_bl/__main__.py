"""Interface for ``python -m dls_backup_bl``."""

from argparse import ArgumentParser
from collections.abc import Sequence

from dls_backup_bl.backup import main as backup_main

from . import __version__

__all__ = ["main"]


def main(args: Sequence[str] | None = None) -> None:
    """Argument parser for the CLI."""
    parser = ArgumentParser()
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=__version__,
    )
    parser.parse_args(args)
    backup_main()


if __name__ == "__main__":
    main()
