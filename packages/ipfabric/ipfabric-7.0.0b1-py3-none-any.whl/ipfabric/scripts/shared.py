import logging
from argparse import ArgumentParser, Namespace

from ipfabric.tools.shared import valid_snapshot


def check_snapshot_arg(snapshot: str) -> str:
    if snapshot.lower() in ["last", "prev", "lastlocked"]:
        snapshot = "$" + snapshot
    snapshot = valid_snapshot(snapshot).strip("'")
    return snapshot


def shared_args(arg_parser: ArgumentParser, logger_name: str) -> Namespace:
    arg_parser.add_argument(
        "-c",
        "--count",
        help="Print count of rows instead of the actual data.",
        action="store_true",
        default=False,
    )
    arg_parser.add_argument(
        "-s",
        "--snapshot",
        help="Snapshot to use which can be a UUID or one of ['last', 'prev', 'lastLocked']"
        "with or without `$` for *nix compatability.",
        default="$last",
    )
    arg_parser.add_argument(
        "-v",
        "--verbose",
        help="Verbose output will enable debugging and print all tables even if no data.",
        action="store_true",
        default=False,
    )
    arg_parser.add_argument(
        "-j",
        "--json",
        help="Enable JSON output which will also print all tables even if no data.",
        action="store_true",
        default=False,
    )
    arg_parser.add_argument(
        "-R",
        "--rich-disable",
        help="Disable rich formatting if installed. Useful for sending JSON output to jq.",
        action="store_true",
        default=False,
    )
    args = arg_parser.parse_args()

    LOGGER = logging.getLogger(logger_name)
    if args.verbose:
        LOGGER.setLevel(logging.DEBUG)
        logging.getLogger("ipfabric").setLevel(logging.DEBUG)
        LOGGER.debug("Logging level set to DEBUG")

    args.snapshot = check_snapshot_arg(args.snapshot)
    LOGGER.debug(f"Snapshot ID selected: {args.snapshot}")
    return args
