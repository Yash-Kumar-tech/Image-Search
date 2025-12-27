import flet as ft

from frontend.src.screens.home_screen import HomeScreen
import sys
from pathlib import Path

sys.path.append(Path.cwd().as_posix())

print(sys.path)

def main(page: ft.Page):
    page.title = "Image Search"
    
    page.theme_mode = ft.ThemeMode.SYSTEM
    home = HomeScreen(page)
    page.add(home)

ft.run(main)
