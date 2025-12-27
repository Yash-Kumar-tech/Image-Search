import os
from pathlib import Path
from typing import Tuple

from backend.db.metadata_db import MetadataDB
from backend.db.vector_db import VectorDB
from backend.models.blip_captioner import BlipCaptioner
from backend.models.clip_embedder import ClipEmbedder
from backend.utils.constants import IMAGE_EXTENSIONS

class Indexer:
    def __init__(self):
        self.captioner = BlipCaptioner()
        self.embeddder = ClipEmbedder()
        self.metadataDb = MetadataDB()
        self.vectorDb = VectorDB()
                
    def indexImage(self, path: Path):
        caption = self.captioner.generateCaption(str(path))
        tags = caption.lower().replace(".", "").split()
        embedding = self.embeddder.encodeImage(str(path))
        self.metadataDb.addImage(path, tags, embedding)
        self.vectorDb.addEmbedding(
            str(path), 
            embedding
        )