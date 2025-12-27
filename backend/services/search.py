from typing import List

from backend.db.metadata_db import MetadataDB
from backend.db.vector_db import VectorDB
from backend.models.clip_embedder import ClipEmbedder
from backend.utils.data_classes import SearchResult


class SearchEngine:
    def __init__(self):
        self.metadataDb = MetadataDB()
        self.vectorDb = VectorDB()
        self.embedder = ClipEmbedder()
    
    def searchByTag(self, query: str) -> List[SearchResult]:
        return self.metadataDb.searchByTag(query)
    
    def searchSemantic(
        self,
        query: str,
        topK: int = 10
    ):
        queryEmb = self.embedder.encodeText(query)
        return self.vectorDb.search(queryEmb, topK = topK)
    
    def searchhybrid(
        self,
        query: str,
        tagFilter: str,
        topK: int = 10
    ):
        tagResults = self.metadataDb.searchByTag(tagFilter)
        queryEmb = self.embedder.encodeText(query)
        semanticResults = self.vectorDb.search(
            queryEmbedding = queryEmb,
            topK = topK
        )
        
        return {
            "tagResults": tagResults,
            "semanticResults": semanticResults
        }