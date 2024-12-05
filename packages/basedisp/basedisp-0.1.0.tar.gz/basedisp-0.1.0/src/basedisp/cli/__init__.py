"""Command line interface for basecon"""

import argparse
from ..utils.functions import clean_inputs
from ..display import display_multiple

__all__ = ["main"]


def parse_args():
    """Parse command line arguments.

    Returns
    -------
    argparse.Namespace
        Parsed command line arguments
    """
    parser = argparse.ArgumentParser(
        description="Process a list of decimal representations"
    )
    parser.add_argument(
        "decimal_representation",
        nargs="*",
        type=str,
        help="List of strings representing decimal values",
    )
    return parser.parse_args()


def main() -> None:
    """Main function to run the number base conversion utility."""
    args: list[str] = parse_args().decimal_representation
    numbers = clean_inputs(args)
    out = display_multiple(numbers)
    print(out)
