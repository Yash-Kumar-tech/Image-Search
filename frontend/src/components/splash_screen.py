import flet as ft
import asyncio

class SplashScreen(ft.Container):
    def __init__(self):
        super().__init__()
        self.expand = True
        self.alignment = ft.Alignment.CENTER
        self.bgcolor = ft.Colors.SURFACE
        
        self.logo = ft.Icon(
            ft.Icons.AUTO_AWESOME_ROUNDED,
            color=ft.Colors.PRIMARY,
            size=80,
            opacity=0,
            animate_opacity=1000,
        )
        
        self.title = ft.Text(
            "Image Search",
            size=32,
            weight=ft.FontWeight.BOLD,
            opacity=0,
            animate_opacity=1000,
            font_family="Inter"
        )
        
        self.status = ft.Text(
            "Initializing neural engines...",
            size=14,
            color=ft.Colors.ON_SURFACE_VARIANT,
            italic=True,
            opacity=0,
            animate_opacity=800,
        )
        
        self.progress = ft.ProgressBar(
            width=200,
            color=ft.Colors.PRIMARY,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            opacity=0,
            animate_opacity=800,
        )
        
        self.content = ft.Column(
            [
                self.logo,
                ft.Container(height=10),
                self.title,
                ft.Container(height=30),
                self.status,
                self.progress
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        )

    async def animateIn(self):
        await asyncio.sleep(0.1)
        self.logo.opacity = 1
        self.title.opacity = 1
        self.update()
        await asyncio.sleep(0.5)
        self.status.opacity = 1
        self.progress.opacity = 1
        self.status.value = "Loading AI Model..."
        self.update()

    def setStatus(self, text: str):
        self.status.value = text
        self.update()
