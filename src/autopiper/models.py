from dataclasses import dataclass


@dataclass
class VoiceModel:
    language: str
    language_code: str
    model_name: str
    quality: str
    onnx_model_link: str
    onnx_model_config_link: str

    @staticmethod
    def from_csv_dict(row_dict: dict) -> "VoiceModel":
        """
        Create a VoiceModel instance from a dictionary representing a CSV row.
        """
        return VoiceModel(
            language=row_dict["Language"],
            language_code=row_dict["LanguageCode"],
            model_name=row_dict["ModelName"],
            quality=row_dict["Quality"],
            onnx_model_link=row_dict["OnnxModelLink"],
            onnx_model_config_link=row_dict["OnnxModelConfigLink"],
        )

    def get_uid(self) -> str:
        """
        Generate a unique identifier for the voice model based on its attributes.
        """
        return f"{self.language_code}-{self.model_name}-{self.quality}"

    def get_filename(self) -> str:
        """
        Generate a filename for the voice model based on its attributes.
        """
        return f"{self.get_uid()}.onnx"

    def get_config_filename(self) -> str:
        """
        Generate a filename for the voice model configuration based on its attributes.
        """
        return f"{self.get_uid()}.onnx.json"

    def __str__(self) -> str:
        """
        String representation of the VoiceModel instance.
        """
        return f"VoiceModel(language={self.language}, language_code={self.language_code}, model_name={self.model_name}, quality={self.quality})"
