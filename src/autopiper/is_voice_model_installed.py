from autopiper import settings
from autopiper.models import VoiceModel


def is_voice_model_installed(voice_model: VoiceModel) -> bool:
    """
    Check if the voice model is installed.

    Args:
        voice_model (VoiceModel): The voice model to check.

    Returns:
        bool: True if the voice model is installed, False otherwise.
    """
    # Check if the model file exists
    model_file_path = settings.APP_ASSET_MODEL_DIR.joinpath(voice_model.get_filename())

    return model_file_path.exists()
