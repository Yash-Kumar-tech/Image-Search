import flet as ft
from pathlib import Path
from typing import Optional, List

class ResultCard(ft.Container):
    def __init__(
        self,
        path: Path,
        tags: Optional[List[str]] = None,
        indexedDate: Optional[str] = None,
        onHover = None
    ):
        super().__init__(
            on_hover = onHover,
            ink = True
        )
        
        # Designing the card
        self.width = 200
        self.padding = 0
        self.margin = 6
        self.border_radius = 12
        self.border = ft.border.all(1, ft.Colors.OUTLINE_VARIANT)
        self.bgcolor = ft.Colors.SURFACE_CONTAINER_HIGHEST
        self.clip_behavior = ft.ClipBehavior.ANTI_ALIAS
        
        self.path = path
        self.tags = tags or []
        self.indexedDate = indexedDate or ""
        
        thumb = ft.Image(
            src = str(path),
            width = 200,
            height = 160,
            fit = ft.BoxFit.COVER,
        )
        
        pathLabel = ft.Text(
            str(path.name),
            size = 14,
            selectable = True,
            weight = ft.FontWeight.W_800,
            overflow = ft.TextOverflow.ELLIPSIS,
            max_lines = 1,
            color = ft.Colors.ON_SURFACE
        )
        
        self.tagsLabel = ft.Text(
            value = ", ".join(self.tags) if self.tags else "No tags",
            size = 12,
            weight = ft.FontWeight.W_600,
            overflow = ft.TextOverflow.ELLIPSIS,
            max_lines = 2,
            width = 180,
            color = ft.Colors.ON_SURFACE_VARIANT
        )
        
        dateLabel = ft.Text(
            value = f"Indexed: {self.indexedDate}",
            size = 11,
            weight = ft.FontWeight.W_500,
            color = ft.Colors.ON_SURFACE_VARIANT
        )
        
        metadataPanel = ft.Container(
            content = ft.Column(
                controls = [pathLabel, self.tagsLabel, dateLabel],
                spacing=1,
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.START
            ),
            padding=ft.padding.only(left=12, right=12, top=6, bottom=10),
        )
 
        # Card layout: image on top, metadata below
        innerColumn = ft.Column(
            controls=[thumb, metadataPanel],
            spacing=0,
            expand = True
        )

        self.content = ft.GestureDetector(
            content=innerColumn,
            on_secondary_tap_down=self.showContextMenu,
        )

    def showContextMenu(self, e: ft.ControlEvent):
        import os
        import subprocess

        def openImage(ev):
            try:
                if os.name == 'nt':
                     os.startfile(self.path)
                else:
                     subprocess.call(['open', str(self.path)])
            except Exception as ex:
                print(f"Error opening image: {ex}")
            finally:
                closeMenu(None)

        def showInFolder(ev):
            try:
                if os.name == 'nt':
                    subprocess.run(['explorer', '/select,', str(self.path)])
                else:
                    subprocess.run(['open', '-R', str(self.path)])
            except Exception as ex:
                print(f"Error showing in folder: {ex}")
            finally:
                closeMenu(None)

        def closeMenu(ev):
            if menuContainer in self.page.overlay:
                self.page.overlay.remove(menuContainer)
            if bgCapturer in self.page.overlay:
                self.page.overlay.remove(bgCapturer)
            self.page.update()

        bgCapturer = ft.GestureDetector(
            on_tap=closeMenu,
            content=ft.Container(bgcolor=ft.Colors.TRANSPARENT),
            expand=True
        )

        def editTags(ev):
            from frontend.src.screens.tags_screen import TagsScreen
            
            def onTagsSaved(newTags):
                self.tags = newTags
                self.tagsLabel.value = ", ".join(newTags) if newTags else "No tags"
                self.update()

            tagsDlg = TagsScreen(self.path, self.tags, onTagsSaved)
            self.page.overlay.append(tagsDlg)
            tagsDlg.open = True
            self.page.update()
            closeMenu(None)

        menuItems = [
            ft.TextButton(
                "Edit Tags", 
                icon=ft.Icons.EDIT_ROUNDED, 
                on_click=editTags,
                style=ft.ButtonStyle(padding=ft.padding.symmetric(horizontal=12, vertical=8))
            ),
            ft.TextButton(
                "Open Image", 
                icon=ft.Icons.IMAGE_OUTLINED, 
                on_click=openImage,
                style=ft.ButtonStyle(padding=ft.padding.symmetric(horizontal=12, vertical=8))
            ),
            ft.TextButton(
                "Show in Folder", 
                icon=ft.Icons.FOLDER_OPEN_ROUNDED, 
                on_click=showInFolder,
                style=ft.ButtonStyle(padding=ft.padding.symmetric(horizontal=12, vertical=8))
            ),
        ]

        # Coordinate extraction with fallbacks for Flet v0.8.0 TapEvent
        try:
            # Priority 0: global_position (x, y) if it exists and is not None
            gp = getattr(e, "global_position", None)
            if gp is not None and hasattr(gp, "x"):
                left = gp.x
                top = gp.y
            else:
                # Priority 1: global_x/y if they exist
                left = getattr(e, "global_x", None)
                top = getattr(e, "global_y", None)
            
            # Priority 2: Parse data string (often "lx ly gx gy" or "gx gy")
            if (left is None or top is None) and hasattr(e, "data") and e.data:
                parts = e.data.split()
                if len(parts) >= 4:
                    left = float(parts[2]) # gx
                    top = float(parts[3])  # gy
                elif len(parts) >= 2:
                    # In some cases data might be just gx gy
                    left = float(parts[0])
                    top = float(parts[1])
            
            # Priority 3: Fallback to local_x/y or defaults
            if left is None: left = getattr(e, "local_x", 100)
            if top is None: top = getattr(e, "local_y", 100)
        except:
            left, top = 100, 100

        menuContainer = ft.Container(
            content=ft.Column(menuItems, tight=True, spacing=0),
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
            border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
            border_radius=8,
            padding=4,
            left=left,
            top=top,
            width=180,
            shadow=ft.BoxShadow(blur_radius=12, color=ft.Colors.with_opacity(0.4, ft.Colors.BLACK)),
            animate_opacity=200
        )

        self.page.overlay.append(bgCapturer)
        self.page.overlay.append(menuContainer)
        self.page.update()
