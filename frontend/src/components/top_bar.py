import flet as ft
from typing import Callable

from frontend.src.screens.index_screen import IndexScreen

class TopBar(ft.Container):
    def __init__(
        self,
        searchCallback: Callable,
        themeCallback: Callable,
        page: ft.Page
    ):
        super().__init__()
        self._page = page
        
        self.padding = ft.padding.symmetric(horizontal=12, vertical=8)
        self.bgcolor = ft.Colors.SURFACE_CONTAINER_LOW
        self.border_radius = 0 # Rectangular TopBar
        self.margin = ft.margin.only(bottom=10)
        self.shadow = None

        # Merged Search Input - Circular Pill Shape with Constant Icon
        self.searchInputField = ft.TextField(
            hint_text="Search by content or tag...",
            expand=True,
            border_radius=30,
            content_padding=ft.padding.symmetric(horizontal=10, vertical=0),
            height=40,
            on_submit=searchCallback,
            bgcolor=ft.Colors.TRANSPARENT,
            border=ft.InputBorder.NONE,
            text_size=14,
        )

        self.searchInput = ft.Container(
            content=ft.Row([
                ft.Container(width=4), # Left spacer
                ft.Icon(ft.Icons.SEARCH_ROUNDED, color=ft.Colors.PRIMARY, size=22),
                self.searchInputField
            ], spacing=0, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            border_radius=30,
            padding=ft.padding.symmetric(horizontal=8),
            shadow=ft.BoxShadow(
                blur_radius=10,
                color=ft.Colors.with_opacity(0.1, ft.Colors.SHADOW),
                offset=ft.Offset(0, 2)
            ),
            expand=True,
            height=44,
        )

        # Backend-only members (preserved as requested)
        self.modeDropdown = ft.Dropdown(value="Semantic", visible=False)
        self.tagFilter = ft.TextField(visible=False)

        # Icon Buttons for Actions
        self.indexBtn = ft.IconButton(
            icon=ft.Icons.ADD_PHOTO_ALTERNATE_OUTLINED,
            on_click=self.openIndexDialog,
            tooltip="Index Images",
            icon_color=ft.Colors.ON_SURFACE_VARIANT
        )
        
        self.tagsBtn = ft.IconButton(
            icon=ft.Icons.TAG_ROUNDED,
            tooltip="Custom Tags",
            icon_color=ft.Colors.ON_SURFACE_VARIANT
        )

        # Theme Toggler (Cycle: System -> Light -> Dark)
        self.theme_modes = ["system", "light", "dark"]
        self.current_theme_index = 0
        self.themeBtn = ft.IconButton(
            icon=ft.Icons.BRIGHTNESS_AUTO_ROUNDED,
            on_click=self.toggleTheme,
            tooltip="Cycle Theme (System/Light/Dark)",
            icon_color=ft.Colors.ON_SURFACE_VARIANT
        )
        
        # We still need a reference for the callback logic if it relies on dropdown value
        self.themeDropdown = ft.Dropdown(value="System", visible=False)
        self.theme_callback = themeCallback

        from backend.services.indexing_manager import IndexingManager
        self.indexing_manager = IndexingManager()
        self.indexing_manager.subscribe(self.update_indexing_status)

        self.indexStatusRing = ft.ProgressRing(width=16, height=16, stroke_width=2, visible=False)
        self.indexStatusText = ft.Text("", size=11, color=ft.Colors.PRIMARY, weight=ft.FontWeight.W_500, visible=False)
        self.indexStatusContainer = ft.Container(
            content=ft.Row([
                self.indexStatusRing,
                self.indexStatusText
            ], spacing=8),
            margin=ft.margin.only(right=10),
            padding=ft.padding.symmetric(horizontal=8, vertical=4),
            border_radius=8,
            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.PRIMARY) if not page.dark_theme else ft.Colors.with_opacity(0.2, ft.Colors.PRIMARY),
            visible=False
        )

        self.content = ft.Row(
            controls=[
                self.searchInput,
                ft.Row(
                    controls=[
                        self.indexStatusContainer,
                        ft.Container(width=1, bgcolor=ft.Colors.OUTLINE_VARIANT, height=24), 
                        self.indexBtn,
                        self.tagsBtn,
                        self.themeBtn,
                    ],
                    spacing=4,
                )
            ],
            spacing=16,
            alignment=ft.MainAxisAlignment.START,
        )
        
        self.indexDlg = IndexScreen()

    def update_indexing_status(self):
        is_indexing = self.indexing_manager.is_indexing
        self.indexStatusContainer.visible = is_indexing
        self.indexStatusRing.visible = is_indexing
        self.indexStatusRing.value = self.indexing_manager.progress
        
        # Simple stats for the text
        if is_indexing:
            self.indexStatusText.visible = True
            self.indexStatusText.value = f"{int(self.indexing_manager.progress * 100)}%"
        else:
            self.indexStatusText.visible = False
            
        try:
            self.update()
        except:
            pass # Handle case where control might not be mounted

    def toggleTheme(self, e):
        self.current_theme_index = (self.current_theme_index + 1) % len(self.theme_modes)
        mode = self.theme_modes[self.current_theme_index]
        
        # Update icon
        icons = {
            "system": ft.Icons.BRIGHTNESS_AUTO_ROUNDED,
            "light": ft.Icons.LIGHT_MODE_ROUNDED,
            "dark": ft.Icons.DARK_MODE_ROUNDED
        }
        self.themeBtn.icon = icons[mode]
        
        # Update dummy dropdown for compat with existing callback
        self.themeDropdown.value = mode.capitalize()
        
        # Trigger callback
        self.theme_callback(e)
        self.update()


    def openIndexDialog(self, e):
        if not self.indexDlg in e.control.page.overlay:
            e.control.page.overlay.append(self.indexDlg)
        self.indexDlg.sync_with_manager()
        self.indexDlg.open = True
        e.control.page.update()