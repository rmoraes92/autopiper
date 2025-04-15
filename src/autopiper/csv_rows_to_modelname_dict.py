from pathlib import Path
from autopiper.read_csv_to_dict import read_csv_to_dict
from autopiper.models import VoiceModel


def csv_rows_to_modelname_dict(csv_file: Path | None = None) -> dict[str, str]:
    """
    Reads a CSV file and converts its rows into a dictionary with ModelName as the key and OnnxModelLink as the value.

    Dict Format:
    {
        "LanguageCode.ModelName.Quality": {
            "OnnxModelLink": "https://....onnx?download=true",
            "OnnxModelConfigLink": "https://....onnx.json?download=true.json"
        }
    }

    Example:
    {
        "ar_JO.kareem.low": {
            "OnnxModelLink": "https://....onnx?download=true",
            "OnnxModelConfigLink": "https://....onnx.json?download=true.json"
        }
    }

    :param csv_file: Path to the CSV file.
    :return: Dictionary where keys are ModelName and values are OnnxModelLink.
    """

    csv_file = csv_file or Path(
        "voices.csv"
    )  # TODO update this to ~/.config/autopiper/voices.csv

    ret = {}

    for row in read_csv_to_dict(csv_file):
        voice_model = VoiceModel.from_csv_dict(row)
        ret[voice_model.get_uid()] = voice_model

    return ret
