import chromadb
from typing import Any
from backend.utils.constants import VECTOR_DB_PATH

class VectorDB:
    def __init__(
        self,
        persistDir: str = VECTOR_DB_PATH
    ):
        # Using PersistentClient for disk storage
        self.client = chromadb.PersistentClient(path=persistDir)
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
        
    def removeEmbedding(self, id: str):
        self.collection.delete(ids=[id])
    
    def search(
        self,
        queryEmbedding: Any,
        topK: int = 10,
    ) -> chromadb.QueryResult:
        return self.collection.query(
            query_embeddings = [queryEmbedding],
            n_results = topK
        )