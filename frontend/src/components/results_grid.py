import flet as ft
from typing import List

from backend.utils.data_classes import SearchResult
from frontend.src.components.result_card import ResultCard

class ResultsGrid(ft.GridView):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.max_extent = 220
        self.spacing = 16
        self.run_spacing = 16
        self.child_aspect_ratio = 0.7
        self.scroll = ft.ScrollMode.AUTO
        self.padding = 20
        
    def showResults(
        self, 
        results: List[SearchResult]
    ):
        self.controls.clear()
        for r in results:
            card = ResultCard(
                path = r.path,
                tags = r.tags,
                indexedDate = r.indexedDate,
                onHover = self.handleCardHover,
            )
            self.controls.append(card)
        self.update()
        
    def handleCardHover(self, e: ft.ControlEvent):
        if e.data == "true":
            e.control.shadow = ft.BoxShadow(
                spread_radius=1,
                blur_radius=12,
                color=ft.Colors.with_opacity(0.2, ft.Colors.SHADOW),
                offset=ft.Offset(0, 4)
            )
            e.control.scale = 1.03
        else:
            e.control.shadow = None
            e.control.scale = 1.0
        e.control.update()