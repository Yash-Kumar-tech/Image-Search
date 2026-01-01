import flet as ft
import asyncio
from pathlib import Path

from backend.services.search import SearchEngine
from frontend.src.components.results_grid import ResultsGrid
from frontend.src.components.top_bar import TopBar

class HomeScreen(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__(expand=True)
        
        self.searchEngine = SearchEngine()
        
        self.topBar = TopBar(
            self.runSearch, 
            self.changeTheme,
            page = page
        )
        self.resultsGrid = ResultsGrid()
        self.resultsGrid.expand = True
        
        self.welcomeLabel = ft.Text(
            "Welcome! Index images and search by tags or content",
            size = 24,
            weight = ft.FontWeight.W_500,
            text_align = ft.TextAlign.CENTER,
            color = ft.Colors.ON_SURFACE_VARIANT
        )

        self.searchSpinner = ft.ProgressRing(
            width=32,
            height=32,
            stroke_width=3,
            visible=False,
            color=ft.Colors.PRIMARY
        )
        
        self.controls = [
            self.topBar,
            ft.Container(
                content=ft.Column([
                    self.welcomeLabel,
                    self.searchSpinner,
                    ft.Container(
                        content=self.resultsGrid, 
                        expand=True,
                        bgcolor=ft.Colors.SURFACE_CONTAINER,
                        border_radius=24,
                        padding=10,
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                expand=True,
                padding=20,
                margin=ft.margin.all(10),
                bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
                border_radius=32,
            )
        ]
        
    async def runSearch(self, e = None):
        query = self.topBar.searchInputField.value.strip()
        
        self.welcomeLabel.visible = False
        self.searchSpinner.visible = True
        self.resultsGrid.visible = False
        self.update()
        
        try:
            # Run model/search in background thread to keep UI alive
            results = await asyncio.to_thread(self.searchEngine.searchHybrid, query, tagFilter=query)
            
            tagResults = results.get("tagResults", [])
            semanticResults = results.get("semanticResults", [])
            
            # Combine unique results by path
            seenPaths = set()
            combined = []
            for r in tagResults + semanticResults:
                if r.path not in seenPaths:
                    combined.append(r)
                    seenPaths.add(r.path)
            
            self.resultsGrid.showResults(combined)
        except Exception as ex:
            print(f"Search Error: {ex}")
        finally:
            self.searchSpinner.visible = False
            self.resultsGrid.visible = True
            self.update()
        
    def changeTheme(self, e):
        pass