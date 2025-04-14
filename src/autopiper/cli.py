import argparse
from autopiper.logger import setup_logger
from autopiper.controllers import download_piper_package

logger = setup_logger()

def main():
    parser = argparse.ArgumentParser(description="cli manager for c++ piper project")

    subparsers = parser.add_subparsers(dest="command")

    init_parser = subparsers.add_parser(
        "init", help="Initialize the project with default settings"
    )
    init_parser.add_argument(
        "--tag-name",
        type=str,
        default=None,
        help="Tag name of the release to download (default: latest)",
    )
    init_parser.set_defaults(func=init_command)

    args = parser.parse_args()
    args.func(args)


def init_command(args: argparse.Namespace) -> None:
    # breakpoint()
    tag_name: str | None = args.tag_name
    logger.info("Project initialized with default settings.")
    download_piper_package(tag_name)


if __name__ == "__main__":
    main()
