from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Any

@dataclass
class SearchResult:
    path: Path
    tags: List[str]
    indexedDate: str
    
    def toDict(self):
        return {
            "path": str(self.path),
            "tags": ",".join(self.tags),
            "indexed_date": self.indexedDate
        }
        
    @classmethod
    def fromDict(cls, res: Dict[str, str]) -> "SearchResult":
        return cls(
            path = Path(res["path"]),
            tags = res["tags"].split(","),
            indexedDate = res["indexed_date"]
        )