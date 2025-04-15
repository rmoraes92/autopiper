import csv
from typing import Generator


def read_csv_to_dict(csv_file) -> Generator[dict, None, None]:
    """
    Reads a CSV file and converts its rows into a list of dictionaries.

    Headers:
    - Language
    - LanguageCode
    - ModelName
    - Quality
    - OnnxModelLink
    - OnnxModelConfigLink

    Example Row:
    Arabic,ar_JO,kareem,low,https://....onnx?download=true,https://....onnx.json?download=true.json

    :param csv_file: Path to the CSV file.
    :return: List of dictionaries where each dictionary represents a row.
    """
    with open(csv_file, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            yield row


# Example usage
if __name__ == "__main__":
    csv_file_path = "voices.csv"
    rows = read_csv_to_dict(csv_file_path)
    for row in rows:
        print(row)
