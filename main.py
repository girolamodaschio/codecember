from src.config import DATA_DIR
from detect_similarities import DuplicateRemover

dirname = DATA_DIR / 'jpg'

# Remove Duplicates
dr = DuplicateRemover(dirname)
dr.find_duplicates()

# Find Similar Images
dr.find_similar("59a89270-d250-429e-975c-4ea417c138be.jpg",70)
