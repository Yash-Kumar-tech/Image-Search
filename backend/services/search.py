from typing import List, Dict
from pathlib import Path

from backend.db.metadata_db import MetadataDB
from backend.db.vector_db import VectorDB
from backend.models.qwen_captioner import QwenCaptioner
from backend.utils.data_classes import SearchResult


class SearchEngine:
    def __init__(self):
        self.metadataDb = MetadataDB()
        self.vectorDb = VectorDB()
        self.model = QwenCaptioner()
    
    def searchByTag(self, query: str) -> List[SearchResult]:
        return self.metadataDb.searchByTag(query)
    
    def searchSemantic(
        self,
        query: str,
        topK: int = 10
    ) -> List[SearchResult]:
        queryEmb = self.model.encodeText(query)
        results = self.vectorDb.search(queryEmb, topK = topK)
        
        sanitized = []
        if results and "ids" in results and results["ids"]:
            ids = results["ids"][0]
            for image_path in ids:
                sanitized.append(SearchResult(
                    path=Path(image_path),
                    tags=[],
                    indexedDate=""
                ))
        return sanitized
    
    def searchhybrid(
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