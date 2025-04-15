from pathlib import Path
from autopiper.read_csv_to_dict import read_csv_to_dict


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
        # Convert the row to a dictionary
        row_dict = dict(row)

        # language = row_dict["Language"]
        languagecode = row_dict["LanguageCode"]
        modelname = row_dict["ModelName"]
        quality = row_dict["Quality"]
        onnxmodellink = row_dict["OnnxModelLink"]
        onnxmodelconfiglink = row_dict["OnnxModelConfigLink"]

        ret[f"{languagecode}.{modelname}.{quality}"] = {
            "OnnxModelLink": onnxmodellink,
            "OnnxModelConfigLink": onnxmodelconfiglink,
        }

    return ret
