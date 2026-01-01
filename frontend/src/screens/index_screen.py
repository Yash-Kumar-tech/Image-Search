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
        
        self.indexingManager = IndexingManager()
        self.indexingManager.subscribe(self.syncWithManager)
        
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
            "Index / Sync Folder",
            on_click = self.handleStartIndexing,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=12),
                padding=20
            ),
            width=float("inf")
        )
        
        self.statusText = ft.Text("Ready", size=12, color=ft.Colors.ON_SURFACE_VARIANT)
        self.progressBar = ft.ProgressBar(width = 500, value = 0, color=ft.Colors.PRIMARY, bgcolor=ft.Colors.SURFACE_CONTAINER)
        
        self.folderList = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, height=200)
        
        self.content = ft.Column([
            ft.Text("Index New Folder", weight=ft.FontWeight.BOLD, size=16),
            ft.Text("Select a folder to scan for images. If the folder is already indexed, it will be synced (updated).", size=13),
            ft.Row([self.folderInput, self.selectBtn], spacing=10),
            self.startBtn,
            ft.Column([
                self.statusText,
                self.progressBar
            ], spacing=5, horizontal_alignment=ft.CrossAxisAlignment.STRETCH),
            ft.Divider(height=30),
            ft.Text("Managed Folders", weight=ft.FontWeight.BOLD, size=16),
            ft.Container(
                content=self.folderList,
                bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
                padding=10,
                border_radius=12,
                border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
                alignment=ft.Alignment.TOP_LEFT,
                width=float("inf") 
            )
        ], tight = True, spacing=15, width=550, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)
        
        self.folderList.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
        
        self.title = ft.Text("Manage Image Folders", weight=ft.FontWeight.W_700)
        self.actions = [
            ft.TextButton("Close", on_click = self.closeDialog)
        ]
        self.actions_alignment = ft.MainAxisAlignment.END

    def selectFolder(self, e):
        if self.indexingManager.isIndexing:
            return
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        folderSelected = filedialog.askdirectory(parent=root, title="Select Images Folder")
        root.destroy()
        
        if folderSelected:
            self.folderInput.value = folderSelected
            self.update()
    
    def syncWithManager(self):
        self.statusText.value = self.indexingManager.status
        self.progressBar.value = self.indexingManager.progress
        self.startBtn.disabled = self.indexingManager.isIndexing
        self.selectBtn.disabled = self.indexingManager.isIndexing
        
        if self.indexingManager.isIndexing:
            if self.indexingManager.currentFolder:
                self.folderInput.value = self.indexingManager.currentFolder
            
        # Update folder list
        self.updateFolderList()
            
        try:
            self.update()
        except:
            pass

    def updateFolderList(self):
        folderStats = self.indexingManager.getIndexedFolders()
        self.folderList.controls.clear()
        
        if not folderStats:
            self.folderList.controls.append(ft.Text("No folders indexed yet", italic=True, size=13, color=ft.Colors.ON_SURFACE_VARIANT))
        else:
            for folder in sorted(folderStats.keys()):
                count = folderStats[folder]
                self.folderList.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.FOLDER_ROUNDED, size=20, color=ft.Colors.PRIMARY),
                            ft.Column([
                                ft.Text(folder, size=13, overflow=ft.TextOverflow.ELLIPSIS, weight=ft.FontWeight.W_500),
                                ft.Text(f"{count} images indexed", size=11, color=ft.Colors.ON_SURFACE_VARIANT),
                            ], expand=True, spacing=0),
                            ft.IconButton(
                                icon=ft.Icons.SYNC_ROUNDED, 
                                tooltip="Sync / Re-index",
                                on_click=lambda e, f=folder: self.syncFolder(f),
                                icon_size=18,
                                disabled=self.indexingManager.isIndexing
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE_ROUNDED, 
                                tooltip="Un-index",
                                on_click=lambda e, f=folder: self.removeFolder(f),
                                icon_size=18,
                                icon_color=ft.Colors.ERROR,
                                disabled=self.indexingManager.isIndexing
                            ),
                        ], spacing=10),
                        padding=ft.padding.symmetric(horizontal=12, vertical=8),
                        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                        border_radius=12
                    )
                )

    def syncFolder(self, folderPath: str):
        self.folderInput.value = folderPath
        asyncio.create_task(self.indexingManager.startIndexing(folderPath))

    def removeFolder(self, folderPath: str):
        asyncio.create_task(self.indexingManager.unindexFolder(folderPath))

    async def handleStartIndexing(self, e):
        folderPath = self.folderInput.value
        if not folderPath:
            return
        asyncio.create_task(self.indexingManager.startIndexing(folderPath))
        
    def closeDialog(self, e):
        self.open = False
        self.update()
