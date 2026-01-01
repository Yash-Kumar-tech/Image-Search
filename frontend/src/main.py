import flet as ft
import asyncio
import os

# Suppress oneDNN custom operations warnings
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

from frontend.src.components.splash_screen import SplashScreen

async def main(page: ft.Page):
    page.title = "AI Image Search"
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.padding = 0
    page.spacing = 0
    page.bgcolor = ft.Colors.SURFACE
    
    # 1. Show Splash Screen
    splash = SplashScreen()
    page.add(splash)
    await splash.animateIn()
    
    # 2. Async Loading of heavy components
    try:
        # Move imports here to avoid blocking splash display
        splash.setStatus("Loading Backend Services...")
        from frontend.src.screens.home_screen import HomeScreen
        
        # Initialize HomeScreen (and Qwen model) in background
        splash.setStatus("Warming up Model and Search Engines...")
        home = await asyncio.to_thread(HomeScreen, page)
        
        # 3. Transition to Home Screen
        splash.setStatus("Almost there...")
        await asyncio.sleep(0.5)
        
        page.clean()
        page.add(home)
        page.update()
        
    except Exception as e:
        splash.setStatus(f"Error: {str(e)}")
        print(f"Error during initialization: {e}")

if __name__ == "__main__":
    ft.run(main)
