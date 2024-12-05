from argparse import ArgumentParser
from typing import Optional, Tuple

from .arguments import Arguments


def process_arguments(args: Optional[Tuple[str, ...]] = None) -> Arguments:
    parser = ArgumentParser()

    parser.add_argument(
        "--log",
        default="DEBUG",
        choices=(
            "DEBUG",
            "INFO",
            "WARNING",
            "CRITICAL",
        ),
        help="log level (default: %(default)s)",
    )

    parser.add_argument(
        "--output_dir",
        type=str,
        default=".",
        help="directory path to save the exported VBA code",
    )

    return Arguments(args=parser.parse_args(args=args))
