import os
from pathlib import Path
import requests

from autopiper import settings
from autopiper import logger
from autopiper.models import VoiceModel


def download_voice_model(voice_model: VoiceModel):
    """
    Downloads a Voice Model (onnx model and onnx json config files).
    """
    # models_dir = Path(os.path.expanduser("~/.config/autopiper/models"))
    models_dir = settings.APP_ASSET_MODEL_DIR
    models_dir.mkdir(parents=True, exist_ok=True)

    # Download the ONNX model
    # --------------------------------------------------------------------------
    model_abs_path = models_dir.joinpath(voice_model.get_filename())

    if not model_abs_path.is_file():
        response = requests.get(voice_model.onnx_model_link, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes

        with model_abs_path.open("wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        logger.debug(
            "Successfully downloaded file from "
            f"{voice_model.onnx_model_link} to {voice_model.get_filename()}"
        )

        # except requests.exceptions.RequestException as e:
        #     print(f"Error downloading file from {url}: {e}")
        # except Exception as e:
        #     print(f"An unexpected error occurred: {e}")
    else:
        logger.debug(f"File {model_abs_path} already exists. Skipping download.")

    # Download the ONNX model config
    # --------------------------------------------------------------------------

    model_config_abs_path = models_dir.joinpath(voice_model.get_config_filename())

    if not model_config_abs_path.is_file():
        response = requests.get(voice_model.onnx_model_config_link, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes

        with model_config_abs_path.open("wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        logger.debug(
            "Successfully downloaded file from "
            f"{voice_model.onnx_model_config_link} to "
            f"{model_config_abs_path}"
        )
    else:
        logger.debug(f"File {model_config_abs_path} already exists. Skipping download.")


if __name__ == "__main__":
    download_url = "https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/ar/ar_JO/kareem/low/ar_JO-kareem-low.onnx?download=true"
    output_filename = "ar_JO-kareem-low.onnx"

    download_voice_model(download_url, output_filename)
