import argparse
from autopiper import logger
from autopiper.controllers import download_piper_package
from autopiper.csv_rows_to_modelname_dict import csv_rows_to_modelname_dict
from autopiper.download_voice_models import download_voice_model
from autopiper.models import VoiceModel


def main() -> None:
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

    lst_models = subparsers.add_parser(
        "list-models",
        help="list onnix mapped models",
    )

    lst_models.set_defaults(func=list_models)

    args = parser.parse_args()
    args.func(args)


def init_command(args: argparse.Namespace) -> None:
    # breakpoint()
    tag_name: str | None = args.tag_name
    logger.info("Project initialized with default settings.")
    download_piper_package(tag_name)
    logger.info("Piper package downloaded successfully.")
    key = f"{args.lang_code}-{args.voice_model_name}-{args.quality}"
    voice_model: VoiceModel = csv_rows_to_modelname_dict()[key]
    download_voice_model(voice_model)
    logger.info(f"voice model link downloaded: {voice_model.onnx_model_link}")
    logger.info(
        f"voice model config link downloaded: {voice_model.onnx_model_config_link}"
    )


def list_models(args: argparse.Namespace) -> None:
    for model_uid_str, _voice_model in csv_rows_to_modelname_dict().items():
        print(model_uid_str)


if __name__ == "__main__":
    main()
