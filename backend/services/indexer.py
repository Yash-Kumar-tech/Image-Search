import os
from pathlib import Path
from typing import List
import spacy

from backend.db.metadata_db import MetadataDB
from backend.db.vector_db import VectorDB
from backend.services.model_factory import ModelFactory

class Indexer:
    def __init__(self):
        self.modelFactory = ModelFactory()
        self.metadataDb = MetadataDB()
        self.vectorDb = VectorDB()
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except:
            self.nlp = None

    @property
    def model(self):
        return self.modelFactory.getActiveModel()
                
    def extractTags(self, caption: str) -> List[str]:
        if not self.nlp:
            return list(set(caption.lower().replace(".", "").split()))
            
        doc = self.nlp(caption)
        tags = []
        for token in doc:
            if token.pos_ in ["NOUN", "PROPN", "ADJ"] and not token.is_stop and token.is_alpha:
                tags.append(token.lemma_.lower())
        
        return list(set(tags))

    def indexImage(self, path: Path):
        caption = self.model.generateCaption(str(path))
        tags = self.extractTags(caption)
        
        embedding = self.model.encodeImage(str(path))
        self.metadataDb.addImage(path, tags, embedding)
        self.vectorDb.addEmbedding(
            str(path), 
            embedding
        )

    def removeImage(self, path: Path):
        self.metadataDb.removeImage(path)
        self.vectorDb.removeEmbedding(str(path))