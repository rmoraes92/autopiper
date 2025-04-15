import os
from pathlib import Path

# TODO maybe try read some of this from a json (or config) file?

APP_ASSET_DIR: Path = Path(os.path.expanduser("~/.local/share/autopiper"))
APP_ASSET_MODEL_DIR: Path = APP_ASSET_DIR.joinpath("models")
CACHE_DIR: Path = Path(os.path.expanduser("~/.cache/autopiper"))
