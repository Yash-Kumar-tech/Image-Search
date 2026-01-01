from pathlib import Path

# Base directory for all data
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp"]

DB_PATH = DATA_DIR / "metadata.db"
VECTOR_DB_PATH = str(DATA_DIR / "vector_store")