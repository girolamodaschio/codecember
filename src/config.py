from decouple import config
from pathlib import Path

ACCOUNT = config("APPLE_ID")
PASSWORD = config("PASSWORD")

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'data'
IMAGE_DIR = DATA_DIR / 'jpg'
DUPLICATES_DIR = DATA_DIR / 'duplicates_dir'
REPORT = 'report'

HASH_SIZE = 8