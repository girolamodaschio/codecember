import glob

from src.config import IMAGE_DIR, HASH_SIZE
from detect_similarities import DuplicateRemover
import time
from PIL import Image
import imagehash

def main():
    dr = DuplicateRemover()
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
                    dr.create_report(file, hashes[temp_hash])

                else:
                    hashes[temp_hash] = file
                    dr.move_files(file, file)
        except Exception as e:
            print(e)

    end_time = time.time()
    print(f"Processing time: {(round(end_time - start_time)/60)}/minutes")


if __name__ == '__main__':
    main()