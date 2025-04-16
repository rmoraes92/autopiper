import argparse
from autopiper import logger
from autopiper.is_voice_model_installed import is_voice_model_installed
from autopiper.download_piper_package import download_piper_package
from autopiper.csv_rows_to_modelname_dict import csv_rows_to_modelname_dict
from autopiper.download_voice_models import download_voice_model
from autopiper.text_to_speech import text_to_speech
from autopiper.models import VoiceModel


def main() -> None:
    parser = argparse.ArgumentParser(description="cli manager for c++ piper project")

    subparsers = parser.add_subparsers(dest="command")

    # Initialize command
    # ==========================================================================

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

    # List models command
    # ==========================================================================

    lst_models = subparsers.add_parser(
        "list-models",
        help="list onnix mapped models",
    )

    lst_models.add_argument(
        "--installed",
        action="store_true",
        help="List installed models",
    )

    lst_models.set_defaults(func=list_models)

    # Text To Speech command
    # ==========================================================================
    tts_parser = subparsers.add_parser(
        "text-to-speech",
        help="Text to speech command",
    )
    tts_parser.add_argument(
        "input_file",
        type=str,
        help="Path to the input text file",
    )
    tts_parser.add_argument(
        "output_file",
        type=str,
        help="Path to the output audio file",
    )
    tts_parser.add_argument(
        "--voide-model-id",
        type=str,
        default="en_US-amy-low",
        help="Voice model ID to use (default: en_US-amy-low)",
    )
    tts_parser.set_defaults(func=tts)

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
    for model_uid_str, voice_model in csv_rows_to_modelname_dict().items():
        if args.installed:
            if is_voice_model_installed(voice_model):
                print(model_uid_str)
        else:
            print(model_uid_str)


def tts(args: argparse.Namespace) -> None:
    # Implement the TTS functionality here
    # For now, just print the arguments
    print(f"Input file: {args.input_file}")
    print(f"Output file: {args.output_file}")
    print(f"Voice model ID: {args.voide_model_id}")
    # Implement the TTS functionality here
    text_to_speech(
        model_uid=args.voide_model_id,
        input_file=args.input_file,
        output_file=args.output_file,
    )


if __name__ == "__main__":
    main()
