import flet as ft
from typing import List

from backend.utils.data_classes import SearchResult
from frontend.src.components.result_card import ResultCard

class ResultsGrid(ft.GridView):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.max_extent = 200
        self.spacing = 10
        self.run_spacing = 10
        self.child_aspect_ratio = 200 / 320
        self.scroll = ft.ScrollMode.AUTO
        
    def showResults(
        self, 
        results: List[SearchResult]
    ):
        self.controls.clear()
        for r in results:
            card = ResultCard(
                path = r.path,
                tags = r.tags,
                indexedDate = r.indexedDate
            )
            self.controls.append(card)
        self.update()