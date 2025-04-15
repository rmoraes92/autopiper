from pathlib import Path
from importlib import resources


def open_asset(filename: Path) -> str:
    filepath = Path("assets", filename)
    if not filename.is_file():
        raise FileNotFoundError(f"asset file does not exist: {filepath}")
    return resources.open_text('autopiper', filepath)
