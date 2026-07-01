from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE_PATH = ROOT_DIR / "configs" / "serve_config.yaml"
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024
