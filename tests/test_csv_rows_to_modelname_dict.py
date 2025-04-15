import unittest
from unittest.mock import patch, MagicMock

from autopiper.csv_rows_to_modelname_dict import csv_rows_to_modelname_dict
from autopiper.models import VoiceModel

# from autopiper.read_csv_to_dict import read_csv_to_dict


class CsvRowsToModelNameDictTestCase(unittest.TestCase):

    @patch("autopiper.csv_rows_to_modelname_dict.read_csv_to_dict")
    def test_csv_rows_to_modelname_dict(
        self,
        mock_read_csv_to_dict,
    ):
        mock_read_csv_to_dict_iter = MagicMock()
        mock_read_csv_to_dict_iter.__iter__.return_value = iter(
            [
                {
                    "Language": "Arabic",
                    "LanguageCode": "ar_JO",
                    "ModelName": "kareem",
                    "Quality": "low",
                    "OnnxModelLink": "https://....onnx?download=true",
                    "OnnxModelConfigLink": "https://....onnx.json?download=true.json",
                },
                # Add other mock rows here
            ]
        )
        mock_read_csv_to_dict.return_value = mock_read_csv_to_dict_iter
        result = csv_rows_to_modelname_dict("tests/test_data/voices.csv")

        self.assertIsNot(result.get("ar_JO-kareem-low"), None)
        self.assertTrue(
            isinstance(result.get("ar_JO-kareem-low"), VoiceModel),
        )
        result = result.get("ar_JO-kareem-low")
        self.assertEqual(result.language, "Arabic")
        self.assertEqual(result.language_code, "ar_JO")
        self.assertEqual(result.model_name, "kareem")
        self.assertEqual(result.quality, "low")
        self.assertEqual(result.onnx_model_link, "https://....onnx?download=true")
        self.assertEqual(
            result.onnx_model_config_link,
            "https://....onnx.json?download=true.json",
        )
        # Check the entire dictionary structure
        self.assertEqual(result.get_uid(), "ar_JO-kareem-low")
        # Check the filename and config filename
        self.assertEqual(result.get_filename(), "ar_JO-kareem-low.onnx")
        self.assertEqual(result.get_config_filename(), "ar_JO-kareem-low.onnx.json")
