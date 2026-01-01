import flet as ft
from pathlib import Path
from typing import Optional, List

class ResultCard(ft.Container):
    def __init__(
        self,
        path: Path,
        tags: Optional[List[str]] = None,
        indexedDate: Optional[str] = None,
        on_hover = None
    ):
        super().__init__(
            on_hover = on_hover,
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
        self.on_secondary_click = self.show_context_menu
        
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
        
        tagsLabel = ft.Text(
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
        
        metadata_panel = ft.Container(
            content = ft.Column(
                controls = [pathLabel, tagsLabel, dateLabel],
                spacing=1,
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.START
            ),
            padding=ft.padding.only(left=12, right=12, top=6, bottom=10),
        )

        # Card layout: image on top, metadata below
        self.content = ft.Column(
            controls=[thumb, metadata_panel],
            spacing=0,
            expand = True
        )

    def show_context_menu(self, e: ft.ControlEvent):
        import os
        import subprocess

        def open_image(ev):
            try:
                if os.name == 'nt':
                     os.startfile(self.path)
                else:
                    subprocess.call(['open', str(self.path)])
            except Exception as ex:
                print(f"Error opening image: {ex}")
            finally:
                close_menu(None)

        def show_in_folder(ev):
            try:
                if os.name == 'nt':
                    subprocess.run(['explorer', '/select,', str(self.path)])
                else:
                    subprocess.run(['open', '-R', str(self.path)])
            except Exception as ex:
                print(f"Error showing in folder: {ex}")
            finally:
                close_menu(None)

        def close_menu(ev):
            if menu_container in self.page.overlay:
                self.page.overlay.remove(menu_container)
            if bg_capturer in self.page.overlay:
                self.page.overlay.remove(bg_capturer)
            self.page.update()

        bg_capturer = ft.GestureDetector(
            on_tap=close_menu,
            content=ft.Container(bgcolor=ft.Colors.TRANSPARENT),
            expand=True
        )

        menu_items = [
            ft.TextButton(
                "Open Image", 
                icon=ft.Icons.IMAGE_OUTLINED, 
                on_click=open_image,
                style=ft.ButtonStyle(padding=ft.padding.symmetric(horizontal=12, vertical=8))
            ),
            ft.TextButton(
                "Show in Folder", 
                icon=ft.Icons.FOLDER_OPEN_ROUNDED, 
                on_click=show_in_folder,
                style=ft.ButtonStyle(padding=ft.padding.symmetric(horizontal=12, vertical=8))
            ),
        ]

        menu_container = ft.Container(
            content=ft.Column(menu_items, tight=True, spacing=0),
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
            border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
            border_radius=8,
            padding=4,
            left=e.global_x,
            top=e.global_y,
            width=180,
            shadow=ft.BoxShadow(blur_radius=12, color=ft.Colors.with_opacity(0.4, ft.Colors.BLACK)),
            animate_opacity=200
        )

        self.page.overlay.append(bg_capturer)
        self.page.overlay.append(menu_container)
        self.page.update()
