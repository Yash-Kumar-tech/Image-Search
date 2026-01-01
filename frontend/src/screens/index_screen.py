import flet as ft
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import asyncio
from backend.services.indexing_manager import IndexingManager

class IndexScreen(ft.AlertDialog):
    def __init__(self):
        super().__init__()
        self.modal = True
        self.shape = ft.RoundedRectangleBorder(radius=28)
        self.content_padding = 24
        
        self.indexing_manager = IndexingManager()
        self.indexing_manager.subscribe(self.sync_with_manager)
        
        self.folderInput = ft.TextField(
            hint_text = "Select folder to index...",
            expand = True,
            border_radius=12,
            read_only=True,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            border=ft.InputBorder.NONE,
            content_padding=16
        )
        
        self.selectBtn = ft.IconButton(
            icon=ft.Icons.FOLDER_OPEN_ROUNDED,
            on_click = self.selectFolder,
            tooltip="Browse Folder",
            icon_color=ft.Colors.PRIMARY
        )
        
        self.startBtn = ft.ElevatedButton(
            "Start Indexing",
            on_click = self.handle_start_indexing,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=12),
                padding=20
            ),
            width=float("inf")
        )
        
        self.statusText = ft.Text("Ready", size=12, color=ft.Colors.ON_SURFACE_VARIANT)
        self.progressBar = ft.ProgressBar(width = 400, value = 0, color=ft.Colors.PRIMARY, bgcolor=ft.Colors.SURFACE_CONTAINER)
        
        self.content = ft.Column([
            ft.Text("Indexing allows you to search through your local images using AI description and tag filtering.", size=14),
            ft.Row([self.folderInput, self.selectBtn], spacing=10),
            ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
            self.startBtn,
            ft.Column([
                self.statusText,
                self.progressBar
            ], spacing=5)
        ], tight = True, spacing=15)
        
        self.title = ft.Text("Index New Images", weight=ft.FontWeight.W_700)
        self.actions = [
            ft.TextButton("Close", on_click = self.closeDialog)
        ]
        self.actions_alignment = ft.MainAxisAlignment.END

    def selectFolder(self, e):
        if self.indexing_manager.is_indexing:
            return
        # Use tkinter for native directory selection on desktop
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        folder_selected = filedialog.askdirectory(parent=root, title="Select Images Folder")
        root.destroy()
        
        if folder_selected:
            self.folderInput.value = folder_selected
            self.update()
    
    def sync_with_manager(self):
        self.statusText.value = self.indexing_manager.status
        self.progressBar.value = self.indexing_manager.progress
        self.startBtn.disabled = self.indexing_manager.is_indexing
        self.selectBtn.disabled = self.indexing_manager.is_indexing
        
        if self.indexing_manager.is_indexing:
            self.folderInput.value = self.indexing_manager.current_folder
            
        try:
            self.update()
        except:
            pass

    async def handle_start_indexing(self, e):
        folder_path = self.folderInput.value
        if not folder_path:
            return
            
        # Trigger background task via manager
        asyncio.create_task(self.indexing_manager.start_indexing(folder_path))
        
    def closeDialog(self, e):
        self.open = False
        self.update()
