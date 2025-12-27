import flet as ft
from pathlib import Path
from backend.services.indexer import Indexer

class IndexScreen(ft.AlertDialog):
    def __init__(self):
        super().__init__()
        
        self.indexer = Indexer()
        
        self.folderInput = ft.TextField(
            hint_text = "Folder path",
            expand = True
        )
        self.selectBtn = ft.ElevatedButton(
            "Browse",
            on_click = self.selectFolder
        )
        self.startBtn = ft.ElevatedButton(
            "Start Indexing",
            on_click = self.startIndexing,
        )
        self.progressBar = ft.ProgressBar(width = 400, value = 0)
        
        self.content = ft.Column([
            ft.Row([self.folderInput, self.selectBtn]),
            self.startBtn,
            self.progressBar
        ], tight = True)
        
        self.title = ft.Text("Index Images")
        self.actions = [ft.TextButton("Close", on_click = self.closeDialog)]
        
    def selectFolder(self, x):
        pass
    
    def startIndexing(self, e):
        folder = Path(self.folderInput.value.strip())
        
        if not folder.exists():
            # self.page.snackBar = ft.SnackBar(ft.Text("Invalid folder path"))
            # self.page.snackBar.open = True
            # self.page.update()
            return
        
        image_exts = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp"}
        images = [p for p in folder.rglob("*") if p.suffix.lower() in image_exts]
        total = len(images)
        if total == 0:
            # self.page.snackBar = ft.SnackBar(ft.Text("No images found"))
            # self.page.snackBar.open = True
            self.page.update()
            return
        
        for i, img in enumerate(images, start = 1):
            try:
                self.indexer.indexImage(img)
            except Exception as ex:
                print(f"Failed: {img} ({ex})")
            self.progressBar.value = i / total
            self.page.update()
        
        # self.page.snackBar = ft.SnackBar(ft.Text("Indexing complete"))
        # self.page.snackBar.open = True
        self.page.update()
        
    def closeDialog(self, e):
        self.open = False