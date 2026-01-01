import flet as ft
from backend.services.settings_manager import SettingsManager

class SettingsScreen(ft.AlertDialog):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.modal = True
        self.title = ft.Text("Settings", weight=ft.FontWeight.W_700)
        self.shape = ft.RoundedRectangleBorder(radius=28)
        self.settingsManager = SettingsManager()
        self._page = page
        
        # Model Selection
        self.modelDropdown = ft.Dropdown(
            label="Active Vision Model",
            options=[
                ft.dropdown.Option("Qwen3-VL-2B"),
                ft.dropdown.Option("Florence-2-Base"),
            ],
            value=self.settingsManager.activeModel,
            width=400,
            border_radius=12,
        )
        # Set on_change explicitly to avoid constructor issues in older Flet versions
        self.modelDropdown.on_change = self.handleModelChange
        
        self.modelInfo = ft.Text(
            "Qwen3-VL-2B: Detailed, high-quality captions and embeddings. (~4-6GB VRAM)\n"
            "Florence-2-Base: Extremely fast, lightweight, good captions. (~1GB VRAM)",
            size=12,
            color=ft.Colors.ON_SURFACE_VARIANT
        )

        self.content = ft.Column([
            ft.Text("Model Configuration", weight=ft.FontWeight.BOLD, size=16),
            self.modelDropdown,
            self.modelInfo,
            ft.Divider(height=20),
            ft.Text("Important: Switching models will change how new images are indexed. Semantic search might not work correctly if different models are used for existing results and the current search.", 
                    size=12, color=ft.Colors.ERROR, weight=ft.FontWeight.W_500),
            ft.Container(height=20),
        ], tight=True, spacing=15)

        self.actions = [
            ft.TextButton("Close", on_click=self.closeDialog)
        ]
        self.actions_alignment = ft.MainAxisAlignment.END

    def handleModelChange(self, e):
        newModel = self.modelDropdown.value
        self.settingsManager.activeModel = newModel
        self._page.snack_bar = ft.SnackBar(
            content=ft.Text(f"Model switched to {newModel}. Indexing will now use this model."),
            action="OK"
        )
        self._page.snack_bar.open = True
        self._page.update()

    def closeDialog(self, e):
        self.open = False
        self.update()
        self._page.update()
