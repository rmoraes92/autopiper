from pathlib import Path
import subprocess

from autopiper import logger
from autopiper import settings


def text_to_speech(model_uid: str, input_file: str, output_file: str) -> None:
    piper_bin_path: Path = settings.APP_ASSET_DIR.joinpath("2023.11.14-2/piper/piper")
    model_file_path: Path = settings.APP_ASSET_MODEL_DIR.joinpath(f"{model_uid}.onnx")
    cmd: str = f"{piper_bin_path} --model {model_file_path} --output_file {output_file}"
    cmd: list[str] = cmd.split()
    input_file_body = open(input_file, "rb")
    proc = subprocess.Popen(
        cmd, stdin=input_file_body, stdout=subprocess.PIPE, text=True
    )
    _output, error = proc.communicate()
    if error:
        logger.error(f"Error: {error}")
