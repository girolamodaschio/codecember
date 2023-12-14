import shutil

from PIL import Image
import imagehash
import os
import numpy as np

from src.config import DUPLICATES_DIR, IMAGE_DIR, REPORT, HASH_SIZE


class DuplicateRemover:
    def __init__(self, hash_size=HASH_SIZE):
        self.hash_size = hash_size

    @staticmethod
    def create_report(origin: str, destination: str) -> None:
        with open(f"{REPORT}.csv", "w") as file:
            file.write(f"{origin}, {destination}\n")

    @staticmethod
    def move_files(origin: str, duplicate: str) -> None:
        origin_filename = origin.split(os.sep)[-1]
        duplicate_filename = duplicate.split(os.sep)[-1]
        directory_path = DUPLICATES_DIR / origin_filename
        os.makedirs(directory_path, exist_ok=True)
        shutil.move(origin, os.path.join(directory_path, origin_filename))
        shutil.move(duplicate, os.path.join(directory_path, duplicate_filename))

    def find_duplicates(self, path):

        hashes = {}
        with Image.open(path) as img:
            temp_hash = imagehash.average_hash(img, self.hash_size)
            if temp_hash in hashes:
                print(f"{path}, {hashes[temp_hash]}")
                self.move_files(path, hashes[temp_hash])
                self.create_report(path, hashes[temp_hash])

    def find_duplicates_concurrent(self):
        pass

    def old_function(self):
        """
        Find and Delete Duplicates
        """
        images_path = [os.path.join(IMAGE_DIR, f) for f in os.listdir(self.dirname)]

        hashes = {}
        duplicates = []

        print("Finding Duplicates Now!\n")
        for image in images_path:
            with Image.open(image) as img:
                temp_hash = imagehash.average_hash(img, self.hash_size)
                if temp_hash in hashes:
                    print("Duplicate {} \nfound for Image {}!\n".format(image, hashes[temp_hash]))
                    duplicates.append(image)
                    origin_file_name = image.split('/')[-1]
                    output_dir = os.path.join(DUPLICATES_DIR, origin_file_name)
                    os.makedirs(output_dir, exist_ok=True)
                    shutil.move(image, os.path.join(output_dir, origin_file_name))
                    duplicate_file_name = os.path.join(IMAGE_DIR, hashes[temp_hash])
                    output_duplicated_filepath = DUPLICATES_DIR / origin_file_name / hashes[temp_hash].split('/')[-1]

                    shutil.move(duplicate_file_name, output_duplicated_filepath)
                else:
                    hashes[temp_hash] = image

    def find_similar(self, location, similarity=80):
        fnames = os.listdir(self.dirname)
        threshold = 1 - similarity / 100
        diff_limit = int(threshold * (self.hash_size ** 2))

        with Image.open(location) as img:
            hash1 = imagehash.average_hash(img, self.hash_size).hash

        print("Finding Similar Images to {} Now!\n".format(location))
        for image in fnames:
            with Image.open(os.path.join(self.dirname, image)) as img:
                hash2 = imagehash.average_hash(img, self.hash_size).hash

                if np.count_nonzero(hash1 != hash2) <= diff_limit:
                    print("{} image found {}% similar to {}".format(image, similarity, location))





