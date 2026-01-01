import flet as ft
from pathlib import Path
from typing import List, Callable, Dict
from backend.db.metadata_db import MetadataDB

class TagsScreen(ft.AlertDialog):
    def __init__(self, imagePath: Path, currentTags: List[str], onSaved: Callable):
        super().__init__()
        self.modal = True
        self.imagePath = imagePath
        self.onSaved = onSaved
        self.db = MetadataDB()

        self.title = ft.Text("Edit Tags", weight=ft.FontWeight.W_700)
        self.shape = ft.RoundedRectangleBorder(radius=28)
        
        # Display image preview
        self.imagePreview = ft.Image(
            src=str(imagePath),
            width=300,
            height=200,
            fit=ft.BoxFit.COVER,
            border_radius=12
        )

        self.tagsInput = ft.TextField(
            label="Tags (comma separated)",
            value=", ".join(currentTags),
            multiline=True,
            min_lines=2,
            max_lines=5,
            border_radius=12,
            hint_text="e.g. nature, mountain, sunset"
        )

        self.content = ft.Column([
            ft.Text(f"File: {imagePath.name}", size=12, italic=True, color=ft.Colors.ON_SURFACE_VARIANT),
            self.imagePreview,
            ft.Container(height=10),
            self.tagsInput,
            ft.Text("Separate tags with commas. Lemmatization and cleaning will be handled automatically if indexed again, but manual edits are preserved as-is.", 
                    size=11, color=ft.Colors.ON_SURFACE_VARIANT)
        ], tight=True, spacing=10, width=400)

        self.actions = [
            ft.TextButton("Cancel", on_click=self.handleCancel),
            ft.ElevatedButton("Save Changes", on_click=self.handleSave, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)))
        ]
        self.actions_alignment = ft.MainAxisAlignment.END

    def handleSave(self, e):
        # Parse tags
        rawText = self.tagsInput.value
        tags = [t.strip().lower() for t in rawText.split(",") if t.strip()]
        
        # Update DB
        self.db.updateTags(self.imagePath, tags)
        
        # Notify callback
        if self.onSaved:
            self.onSaved(tags)
            
        self.open = False
        self.update()
        self.page.update()

    def handleCancel(self, e):
        self.open = False
        self.update()
        self.page.update()

class GlobalTagsScreen(ft.AlertDialog):
    def __init__(self):
        super().__init__()
        self.modal = True
        self.db = MetadataDB()
        self.title = ft.Text("Custom Tags Manager", weight=ft.FontWeight.W_700)
        self.shape = ft.RoundedRectangleBorder(radius=28)
        self.content_padding = 24
        
        self.imageList = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, height=400)
        
        self.content = ft.Column([
            ft.Text("Manually edit tags for all indexed images.", size=13),
            ft.Container(
                content=self.imageList,
                bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
                padding=10,
                border_radius=12,
                border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
                width=600
            )
        ], tight=True, spacing=15)
        
        self.actions = [
            ft.TextButton("Close", on_click=self.closeDialog)
        ]
        self.actions_alignment = ft.MainAxisAlignment.END

    def updateImageList(self):
        images = self.db.getAllImages()
        self.imageList.controls.clear()
        
        if not images:
            self.imageList.controls.append(ft.Text("No images indexed yet", italic=True, size=13, color=ft.Colors.ON_SURFACE_VARIANT))
        else:
            for img in images:
                self.imageList.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Image(src=str(img.path), width=50, height=50, fit=ft.BoxFit.COVER, border_radius=8),
                            ft.Column([
                                ft.Text(img.path.name, size=13, weight=ft.FontWeight.BOLD, overflow=ft.TextOverflow.ELLIPSIS),
                                ft.Text(", ".join(img.tags) if img.tags else "No tags", size=11, color=ft.Colors.ON_SURFACE_VARIANT, overflow=ft.TextOverflow.ELLIPSIS),
                            ], expand=True, spacing=2),
                            ft.IconButton(
                                icon=ft.Icons.EDIT_ROUNDED,
                                tooltip="Edit Tags",
                                on_click=lambda e, i=img: self.openTagsEditor(i),
                                icon_size=20
                            )
                        ], spacing=10),
                        padding=10,
                        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                        border_radius=12
                    )
                )

    def openTagsEditor(self, img):
        def onSaved(newTags):
            # Refresh list after editing
            self.updateImageList()
            self.update()

        tagsDlg = TagsScreen(img.path, img.tags, onSaved)
        self.page.overlay.append(tagsDlg)
        tagsDlg.open = True
        self.page.update()

    def closeDialog(self, e):
        self.open = False
        self.update()
