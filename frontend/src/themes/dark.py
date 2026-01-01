import flet as ft

def get_dark_theme():
    return ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.Colors.BLUE_200,
            on_primary=ft.Colors.BLUE_900,
            primary_container=ft.Colors.BLUE_800,
            on_primary_container=ft.Colors.BLUE_50,
            secondary=ft.Colors.AMBER_200,
            on_secondary=ft.Colors.AMBER_900,
            surface=ft.Colors.BLUE_GREY_900,
            on_surface=ft.Colors.BLUE_GREY_50,
            outline=ft.Colors.BLUE_GREY_700,
            surface_container_highest=ft.Colors.BLUE_GREY_800,
        ),
        visual_density=ft.VisualDensity.COMFORTABLE,
        font_family="Inter",
    )
