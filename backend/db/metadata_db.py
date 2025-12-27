import json
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List, Any, Optional

from backend.utils.constants import DB_PATH
from backend.utils.data_classes import SearchResult

class MetadataDB:
    def __init__(
        self,
        dbPath: Path = DB_PATH
    ):
        self.dbPath = dbPath
        self._initDb()
        
    def _connectToDb(self):
        return sqlite3.connect(self.dbPath)
    
    def _initDb(self):
        conn = self._connectToDb()
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS images (
                path TEXT PRIMARY KEY,
                tags TEXT,
                embedding BLOB,
                indexed_date TEXT
            )
        """)
        conn.commit()
        conn.close()
        
    def addImage(
        self,
        path: Path,
        tags: List[str],
        embedding: Any,
        indexedDate: Optional[str] = None
    ):
        conn = self._connectToDb()
        c = conn.cursor()
        tagsStr = ",".join(tags) if isinstance(tags, list) else str(tags)
        embeddingStr = json.dumps(embedding)
        if indexedDate is None:
            indexedDate = datetime.now().isoformat(timespec="seconds")
        
        c.execute("""
            INSERT OR REPLACE INTO images (path, tags, embedding, indexed_date)
            VALUES (?, ?, ?, ?)
        """, (str(path), tagsStr, embeddingStr, indexedDate))
        conn.commit()
        conn.close()
        
    def searchByTag(self, query: str):
        conn = self._connectToDb()
        c = conn.cursor()
        c.execute("""
            SELECT path, tags, indexed_date FROM images WHERE tags LIKE ?
        """, (f"%{query}%", ))
        rows = c.fetchall()
        conn.close()
        return [SearchResult(
            path = Path(r[0]),
            tags = r[1].split(",") if r[1] else [],
            indexedDate = r[2]
        ) for r in rows]