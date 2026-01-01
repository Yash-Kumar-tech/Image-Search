import asyncio
from pathlib import Path
from typing import List, Callable, Optional
from backend.services.indexer import Indexer

class IndexingManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(IndexingManager, cls).__new__(cls)
            cls._instance._is_indexing = False
            cls._instance._progress = 0.0
            cls._instance._status = "Ready"
            cls._instance._current_folder = None
            cls._instance._subscribers = []
            cls._instance._indexer = Indexer()
        return cls._instance

    @property
    def is_indexing(self) -> bool:
        return self._is_indexing

    @property
    def progress(self) -> float:
        return self._progress

    @property
    def status(self) -> str:
        return self._status

    @property
    def current_folder(self) -> Optional[str]:
        return self._current_folder

    def subscribe(self, callback: Callable):
        if callback not in self._subscribers:
            self._subscribers.append(callback)

    def unsubscribe(self, callback: Callable):
        if callback in self._subscribers:
            self._subscribers.remove(callback)

    def _notify(self):
        for callback in self._subscribers:
            try:
                callback()
            except Exception as e:
                print(f"Error notifying subscriber: {e}")

    async def start_indexing(self, folder_path: str):
        if self._is_indexing:
            return

        self._is_indexing = True
        self._current_folder = folder_path
        self._progress = 0.0
        self._status = "Initializing..."
        self._notify()

        try:
            folder = Path(folder_path)
            image_exts = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp"}
            images = [p for p in folder.rglob("*") if p.suffix.lower() in image_exts]
            total = len(images)

            if total == 0:
                self._status = "No supported images found"
                self._is_indexing = False
                self._notify()
                return

            for i, img in enumerate(images, start=1):
                self._status = f"Processing {i}/{total}: {img.name}"
                self._notify()
                
                # Run the blocking indexing call in a separate thread
                await asyncio.to_thread(self._indexer.indexImage, img)
                
                self._progress = i / total
                self._notify()

            self._status = f"Indexing complete! {total} images processed."
        except Exception as e:
            self._status = f"Error: {str(e)}"
        finally:
            self._is_indexing = False
            self._notify()
