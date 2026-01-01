import flet as ft
from frontend.src.screens.home_screen import HomeScreen
import sys
from pathlib import Path
import asyncio

sys.path.append(Path.cwd().as_posix())

from frontend.src.themes.light import get_light_theme
from frontend.src.themes.dark import get_dark_theme
from frontend.src.components.splash_screen import SplashScreen

async def main(page: ft.Page):
    page.title = "Image Search"
    page.fonts = {
        "Inter": "https://github.com/google/fonts/raw/main/ofl/inter/Inter%5Bslnt%2Cwght%5D.ttf"
    }
    
    page.theme = get_light_theme()
    page.dark_theme = get_dark_theme()
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.padding = 0
    page.spacing = 0
    
    # 1. Show Splash Screen
    splash = SplashScreen()
    page.add(splash)
    await splash.animate_in()
    
    splash.set_status("Initializing backend engines (Qwen-VL)...")
    
    try:
        # Load HomeScreen in background thread to keep splash alive
        home = await asyncio.to_thread(HomeScreen, page)
        
        splash.set_status("Ready!")
        await asyncio.sleep(0.5)
        
        page.clean()
        page.add(home)
    except Exception as e:
        splash.set_status(f"Startup error: {e}")
        print(f"Error during initialization: {e}")

if __name__ == "__main__":
    ft.run(main)
