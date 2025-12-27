import chromadb
from chromadb.config import Settings
from typing import Any, Dict
from backend.utils.constants import VECTOR_DB_PATH
from backend.utils.data_classes import SearchResult

class VectorDB:
    def __init__(
        self,
        persistDir: str = VECTOR_DB_PATH
    ):
        self.client = chromadb.Client(
            Settings(
                # persist_dir = persistDir
            )
        )
        self.collection = self.client.get_or_create_collection("images")
        
    def addEmbedding(
        self,
        id: str,
        embedding: Any,
    ):
        self.collection.add(
            ids = [id],
            embeddings = [embedding],
        )
    
    def search(
        self,
        queryEmbedding: Any,
        topK: int = 10,
    ) -> chromadb.QueryResult:
        return self.collection.query(
            query_embeddings = [queryEmbedding],
            n_results = topK
        )