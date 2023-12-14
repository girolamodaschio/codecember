import glob
import os

from src.config import IMAGE_DIR, HASH_SIZE, DUPLICATES_DIR
from detect_similarities import Codecember
import time
from PIL import Image
import imagehash


def generate_report():
    counter = 0
    for dir in os.listdir(DUPLICATES_DIR):
        if len(os.listdir(os.path.join(DUPLICATES_DIR, dir))) > 1:
            counter +=1
    ratio = counter / len(os.listdir(DUPLICATES_DIR))
    print(f"Duplicates found: {counter}\nRatio: {ratio}")


def main():
    dr = Codecember()
    hashes = {}
    counter = 0
    files = glob.glob(f'{IMAGE_DIR}/*')

    start_time = time.time()
    for file in files:
        counter += 1
        print(f"{counter} / {len(files)}")
        try:
            with Image.open(file) as img:
                temp_hash = imagehash.average_hash(img, hash_size=HASH_SIZE)
                if temp_hash in hashes:
                    dr.move_files(file, hashes[temp_hash])
                else:
                    hashes[temp_hash] = file
                    dr.move_files(file, file)
        except Exception as e:
            print(e)

    end_time = time.time()
    print(f"Processing time: {(round(end_time - start_time)/60)}/minutes")
    generate_report()


if __name__ == '__main__':
    main()
    generate_report()