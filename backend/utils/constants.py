from typing import Literal
from pathlib import Path

IMAGE_EXTENSIONS = Literal[".jpg", ".jpeg", ".png"]

DB_PATH = Path("data/metadata.db")

VECTOR_DB_PATH = "data/vector_store"