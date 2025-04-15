import unittest
from unittest.mock import patch, MagicMock

from autopiper.csv_rows_to_modelname_dict import csv_rows_to_modelname_dict
# from autopiper.read_csv_to_dict import read_csv_to_dict


class CsvRowsToModelNameDictTestCase(unittest.TestCase):

    @patch("autopiper.csv_rows_to_modelname_dict.read_csv_to_dict")
    def test_csv_rows_to_modelname_dict(
        self,
        mock_read_csv_to_dict,
    ):
        mock_read_csv_to_dict_iter = MagicMock()
        mock_read_csv_to_dict_iter.__iter__.return_value = iter([
            {
                "Language": "Arabic",
                "LanguageCode": "ar_JO",
                "ModelName": "kareem",
                "Quality": "low",
                "OnnxModelLink": "https://....onnx?download=true",
                "OnnxModelConfigLink": "https://....onnx.json?download=true.json",
            },
            # Add other mock rows here
        ])
        mock_read_csv_to_dict.return_value = mock_read_csv_to_dict_iter
        result = csv_rows_to_modelname_dict("tests/test_data/voices.csv")
        expected_result = {
            "kareem": {
                "Language": "Arabic",
                "LanguageCode": "ar_JO",
                "Quality": "low",
                "OnnxModelLink": "https://....onnx?download=true",
                "OnnxModelConfigLink": "https://....onnx.json?download=true.json",
            },
            # Add other expected results here
        }
        self.assertEqual(result, expected_result)
