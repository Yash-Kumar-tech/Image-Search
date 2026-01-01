import flet as ft

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
        
        self.controls = [
            self.topBar,
            ft.Container(
                content=ft.Column([
                    self.welcomeLabel,
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
        
    def runSearch(self, e = None):
        query = self.topBar.searchInputField.value.strip()
        
        self.welcomeLabel.visible = False
        
        # Merge search uses Hybrid by default (searching both content and tags)
        # We pass the same query for both tag filter and semantic query
        results = self.searchEngine.searchhybrid(query, tagFilter=query)
        
        # If it's a dict (from searchhybrid), we extract results or just show them if the grid supports it
        # Actually searchhybrid returns {"tagResults": ..., "semanticResults": ...}
        # But for the UI, we might want to merge them.
        
        # Let's fix searchhybrid return type or handle it here
        tag_results = results.get("tagResults", [])
        semantic_results = results.get("semanticResults", [])
        
        # Combine unique results by path
        seen_paths = set()
        combined = []
        for r in tag_results + semantic_results:
            if r.path not in seen_paths:
                combined.append(r)
                seen_paths.add(r.path)
        
        self.resultsGrid.showResults(combined)
        
    def changeTheme(self, e):
        selected = self.topBar.themeDropdown.value.lower() # type: ignore
        if selected == "dark":
            self.page.theme_mode = ft.ThemeMode.DARK
        elif selected == "light":
            self.page.theme_mode = ft.ThemeMode.LIGHT
        else:
            self.page.theme_mode = ft.ThemeMode.SYSTEM
        self.page.update()