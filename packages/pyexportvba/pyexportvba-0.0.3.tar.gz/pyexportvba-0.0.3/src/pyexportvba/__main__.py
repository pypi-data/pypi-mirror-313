import logging
import os
import sys
from pprint import pformat
from typing import Optional, Tuple

from .arguments import process_arguments
from .export_vba import export_vba_from_excel_app


def main(args: Optional[Tuple[str, ...]] = None) -> int:

    p_args = process_arguments(args=args)

    logging.basicConfig(level=logging.INFO)

    logger = logging.getLogger(__name__)

    logger.info(
        "System paths:\n%s",
        pformat(
            os.environ["PATH"].split(":"),
            indent=2,
        ),
    )
    logger.info(
        "Python paths:\n%s",
        pformat(
            sys.path,
            indent=2,
        ),
    )
    logger.info(p_args.get_arguments_summary())

    logger.info("using output path %s", p_args.output_dir)

    export_vba_from_excel_app(p_args.output_dir)

    return 0


if __name__ == "__main__":
    sys.exit(main())
