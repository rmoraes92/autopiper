import argparse
from autopiper import logger
from autopiper.controllers import download_piper_package
from autopiper.csv_rows_to_modelname_dict import csv_rows_to_modelname_dict

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
    init_parser.add_argument(
        "--lang-code",
        type=str,
        default="en_US",
        help="Language code to use (default: en_US)",
    )
    init_parser.add_argument(
        "--voice-model-name",
        type=str,
        default="amy",
        help="Voice name to use (default: amy)",
    )
    init_parser.add_argument(
        "--quality",
        type=str,
        default="low",
        help="Quality of the voice model (default: low)",
    )
    init_parser.set_defaults(func=init_command)

    args = parser.parse_args()
    args.func(args)


def init_command(args: argparse.Namespace) -> None:
    # breakpoint()
    tag_name: str | None = args.tag_name
    logger.info("Project initialized with default settings.")
    download_piper_package(tag_name)
    logger.info("Piper package downloaded successfully.")
    key = f"{args.lang_code}.{args.voice_model_name}.{args.quality}"
    d = csv_rows_to_modelname_dict()[key]
    logger.info(f"Model link: {d['OnnxModelLink']}")
    logger.info(f"Model config link: {d['OnnxModelConfigLink']}")


if __name__ == "__main__":
    main()
