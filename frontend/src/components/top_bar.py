import flet as ft
from typing import Callable

from frontend.src.screens.index_screen import IndexScreen

class TopBar(ft.Row):
    def __init__(
        self,
        searchCallback: Callable,
        themeCallback: Callable,
        page: ft.Page
    ):
        super().__init__()
        self._page = page 
        self.searchInput = ft.TextField(
            hint_text = "Search image...",
            expand = True
        )
        self.modeDropdown = ft.Dropdown(
            options = [
                ft.dropdown.Option("Tag"),
                ft.dropdown.Option("Semantic"),
                ft.dropdown.Option("Hybrid"),
            ],
            value = "Tag"
        )
        
        self.tagFilter = ft.TextField(
            hint_text = "Tag filter (hybrid only)",
            width = 200
        )
        self.searchBtn = ft.ElevatedButton("Search", on_click = searchCallback)
        self.indexBtn = ft.ElevatedButton(
            "Index",
            on_click = self.openIndexDialog
        )
        self.tagsBtn = ft.ElevatedButton("Custom Tags")
        self.themeDropdown = ft.Dropdown(
            options = [
                ft.dropdown.Option("System"),
                ft.dropdown.Option("Dark"),
                ft.dropdown.Option("Light"),
            ],
            value = "Light",
            on_text_change = themeCallback
        )
        
        self.controls = [
            self.searchInput,
            self.modeDropdown,
            self.tagFilter,
            self.searchBtn,
            self.indexBtn,
            self.tagsBtn,
            self.themeDropdown
        ]
        self.indexDlg = IndexScreen()

    def openIndexDialog(self, e):
        if not self.indexDlg in e.control.page.overlay:
            e.control.page.overlay.append(self.indexDlg)
        self.indexDlg.open = True
        e.control.page.update()