import flet as ft

from backend.services.search import SearchEngine
from frontend.src.components.results_grid import ResultsGrid
from frontend.src.components.top_bar import TopBar

class HomeScreen(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        
        self.searchEngine = SearchEngine()
        
        self.topBar = TopBar(
            self.runSearch, 
            self.changeTheme,
            page = page
        )
        self.resultsGrid = ResultsGrid()
        self.resultsGrid.expand = True
        
        self.welcomeLabel = ft.Text(
            "Welcome! Index imagesa and search by tags or content",
            size = 20,
            text_align = ft.TextAlign.CENTER
        )
        
        self.controls = [
            self.topBar,
            self.welcomeLabel,
            ft.Container(self.resultsGrid, expand=True)
        ]
        
    def runSearch(self, e = None):
        query = self.topBar.searchInput.value.strip()
        mode = self.topBar.modeDropdown.value.lower() # type: ignore
        tagFilter = self.topBar.tagFilter.value.strip()
        
        self.welcomeLabel.visible = False
        
        if mode == "tag":
            results = self.searchEngine.searchByTag(query)
        elif mode == "semantic":
            results = self.searchEngine.searchSemantic(query)
        else:
            results = self.searchEngine.searchhybrid(query, tagFilter)
        
        self.resultsGrid.showResults(results)  # type: ignore
        
    def changeTheme(self, e):
        selected = self.topBar.themeDropdown.value.lower() # type: ignore
        if selected == "dark":
            self.page.theme_mode = ft.ThemeMode.DARK
        elif selected == "light":
            self.page.theme_mode = ft.ThemeMode.LIGHT
        else:
            self.page.theme_mode = ft.ThemeMode.SYSTEM
        self.page.update()