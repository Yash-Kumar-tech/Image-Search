import asyncio
from pathlib import Path
from typing import List, Callable, Optional, Dict
from backend.services.indexer import Indexer

class IndexingManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(IndexingManager, cls).__new__(cls)
            cls._instance._isIndexing = False
            cls._instance._progress = 0.0
            cls._instance._status = "Ready"
            cls._instance._currentFolder = None
            cls._instance._subscribers = []
            cls._instance._indexer = Indexer()
        return cls._instance

    @property
    def isIndexing(self) -> bool:
        return self._isIndexing

    @property
    def progress(self) -> float:
        return self._progress

    @property
    def status(self) -> str:
        return self._status

    @property
    def currentFolder(self) -> Optional[str]:
        return self._currentFolder

    def subscribe(self, callback: Callable):
        if callback not in self._subscribers:
            self._subscribers.append(callback)

    def unsubscribe(self, callback: Callable):
        if callback in self._subscribers:
            self._subscribers.remove(callback)

    def notifySubscribers(self):
        for callback in self._subscribers:
            try:
                callback()
            except Exception as e:
                print(f"Error notifying subscriber: {e}")

    def getIndexedFolders(self) -> Dict[str, int]:
        """Returns a dict of {folderPath: imageCount}."""
        allImages = self._indexer.metadataDb.getAllImages()
        folderStats = {}
        for img in allImages:
             parent = str(img.path.parent)
             folderStats[parent] = folderStats.get(parent, 0) + 1
        return folderStats

    async def unindexFolder(self, folderPath: str):
        """Removes all images in the specified folder from the index."""
        if self._isIndexing: return
        
        self._isIndexing = True
        self._status = f"Unindexing {folderPath}..."
        self._progress = 0.0
        self.notifySubscribers()
        
        try:
            imagesInDb = self._indexer.metadataDb.getImagesInFolder(folderPath)
            total = len(imagesInDb)
            if total == 0:
                self._status = "No images found in index for this folder"
                return

            for i, img in enumerate(imagesInDb, start=1):
                self._indexer.removeImage(img.path)
                self._progress = i / total
                self.notifySubscribers()
            self._status = "Unindexing complete"
        except Exception as e:
            self._status = f"Error: {str(e)}"
        finally:
            self._isIndexing = False
            self.notifySubscribers()

    async def startIndexing(self, folderPath: str):
        """Syncs the folder: adds new images, updates changed ones, removes missing ones."""
        if self._isIndexing:
            return

        self._isIndexing = True
        self._currentFolder = folderPath
        self._progress = 0.0
        self._status = "Scanning folder..."
        self.notifySubscribers()

        try:
            folder = Path(folderPath)
            from backend.utils.constants import IMAGE_EXTENSIONS
            imageExts = set(IMAGE_EXTENSIONS)
            
            # 1. Scan disk
            onDiskPaths = {p for p in folder.rglob("*") if p.suffix.lower() in imageExts}
            
            # 2. Query DB for existing images in this folder
            inDbResults = self._indexer.metadataDb.getImagesInFolder(folderPath)
            inDbPaths = {res.path for res in inDbResults}
            
            # 3. Determine work
            toAdd = onDiskPaths - inDbPaths
            toRemove = inDbPaths - onDiskPaths
            
            # We treat all "on disk" as things to process (to ensure 'update' works)
            toProcess = list(onDiskPaths) 
            totalWork = len(toProcess) + len(toRemove)
            
            if totalWork == 0:
                self._status = "Folder already up to date"
                self._isIndexing = False
                self.notifySubscribers()
                return

            processedCount = 0

            # Step A: Remove missing images
            for i, path in enumerate(toRemove, start=1):
                self._status = f"Removing missing: {path.name}"
                self.notifySubscribers()
                await asyncio.to_thread(self._indexer.removeImage, path)
                processedCount += 1
                self._progress = processedCount / totalWork
                self.notifySubscribers()

            # Step B: Index/Re-index active images
            for i, img in enumerate(toProcess, start=1):
                self._status = f"Indexing {i}/{len(toProcess)}: {img.name}"
                self.notifySubscribers()
                
                await asyncio.to_thread(self._indexer.indexImage, img)
                
                processedCount += 1
                self._progress = processedCount / totalWork
                self.notifySubscribers()

            self._status = f"Sync complete! {len(toProcess)} active, {len(toRemove)} removed."
        except Exception as e:
            self._status = f"Error: {str(e)}"
        finally:
            self._isIndexing = False
            self.notifySubscribers()
