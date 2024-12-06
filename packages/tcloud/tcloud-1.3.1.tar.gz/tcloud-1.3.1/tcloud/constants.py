import os
from pathlib import Path


TCLOUD_PATH = Path(os.environ.get("TCLOUD_HOME", Path.home() / ".tcloud"))
EXTRAS_PATH = TCLOUD_PATH / ".extras.yaml"
