import flet as ft
from pathlib import Path
from typing import Optional, List

class ResultCard(ft.Container):
    def __init__(
        self,
        path: Path,
        tags: Optional[List[str]] = None,
        indexedDate: Optional[str] = None
    ):
        super().__init__(
            on_hover = self._onHover,
            ink = True
        )
        
        # Designing the card
        self.width = 200
        self.padding = 0
        self.margin = 6
        self.border_radius = 8
        self.border = ft.border.all(1, "black")
        self.bgcolor = ft.Colors.WHITE
        
        self.path = path
        self.tags = tags or []
        self.indexedDate = indexedDate or ""
        
        thumb = ft.Image(
            src = str(path),
            width = 200,
            height = 160,
            fit = ft.BoxFit.COVER,
            border_radius = ft.border_radius.only(top_left = 8, top_right = 8)
        )
        
        pathLabel = ft.Text(
            str(path.name),
            size = 12,
            selectable = True,
            weight = ft.FontWeight.BOLD,
            overflow = ft.TextOverflow.ELLIPSIS,
            max_lines = 1,
        )
        
        tagsLabel = ft.Text(
            value = ", ".join(self.tags),
            size = 11,
            italic = True,
            overflow = ft.TextOverflow.ELLIPSIS,
            max_lines = 2,
            width = 180,
        )
        
        dateLabel = ft.Text(
            value = f"Indexed: {self.indexedDate}",
            size = 10,
        )
        
        metadata_panel = ft.Container(
            content = ft.Column(
                controls = [pathLabel, tagsLabel, dateLabel],
                spacing=4,
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.START
            ),
            padding=8,
            bgcolor=ft.Colors.GREY_100,
            border_radius=ft.border_radius.only(bottom_left=8, bottom_right=8)
        )

        # Card layout: image on top, metadata below
        self.content = ft.Column(
            controls=[thumb, metadata_panel],
            spacing=0,
            expand = True
        )
        
        # self.on_hover = self._onHover
        
    def _onHover(self, e: ft.HoverEvent):
        if e.data == "true":
            self.shadow = ft.BoxShadow(
                spread_radius=1,
                blur_radius=8,
                color=ft.Colors.BLUE_GREY_200,
                offset=ft.Offset(0, 2)
            )
            self.scale = 1.03  # slight zoom
        else:
            self.shadow = None
            self.scale = 1.0
        self.update()