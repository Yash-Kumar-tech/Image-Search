from typing import List, Dict
from pathlib import Path

from backend.db.metadata_db import MetadataDB
from backend.db.vector_db import VectorDB
from backend.services.model_factory import ModelFactory
from backend.utils.data_classes import SearchResult


class SearchEngine:
    def __init__(self):
        self.metadataDb = MetadataDB()
        self.vectorDb = VectorDB()
        self.modelFactory = ModelFactory()
    
    @property
    def model(self):
        return self.modelFactory.getActiveModel()
    
    def searchByTag(self, query: str) -> List[SearchResult]:
        return self.metadataDb.searchByTag(query)
    
    def searchSemantic(
        self,
        query: str,
        topK: int = 10
    ) -> List[SearchResult]:
        queryEmbedding = self.model.encodeText(query)
        results = self.vectorDb.search(queryEmbedding, topK = topK)
        
        sanitized = []
        if results and "ids" in results and results["ids"]:
            ids = results["ids"][0]
            for imagePath in ids:
                sanitized.append(SearchResult(
                    path=Path(imagePath),
                    tags=[],
                    indexedDate=""
                ))
        return sanitized
    
    def searchHybrid(
        self,
        query: str,
        tagFilter: str,
        topK: int = 10
    ) -> Dict[str, List[SearchResult]]:
        tagResults = self.metadataDb.searchByTag(tagFilter)
        semanticResults = self.searchSemantic(query, topK=topK)
        
        return {
            "tagResults": tagResults,
            "semanticResults": semanticResults
        }