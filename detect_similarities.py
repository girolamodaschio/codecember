import shutil

from PIL import Image
import imagehash
import os
import numpy as np

from src.config import DUPLICATES_DIR, IMAGE_DIR, REPORT, HASH_SIZE


class Codecember:
    def __init__(self, hash_size=HASH_SIZE):
        self.hash_size = hash_size

    @staticmethod
    def move_files(origin: str, duplicate: str) -> None:
        origin_filename = origin.split(os.sep)[-1]
        duplicate_filename = duplicate.split(os.sep)[-1]
        directory_path = DUPLICATES_DIR / origin_filename
        os.makedirs(directory_path, exist_ok=True)
        shutil.move(origin, os.path.join(directory_path, origin_filename))
        shutil.move(duplicate, os.path.join(directory_path, duplicate_filename))




