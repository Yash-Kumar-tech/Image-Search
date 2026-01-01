import flet as ft

def get_light_theme():
    return ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.Colors.BLUE_600,
            on_primary=ft.Colors.WHITE,
            primary_container=ft.Colors.BLUE_100,
            on_primary_container=ft.Colors.BLUE_900,
            secondary=ft.Colors.AMBER_600,
            on_secondary=ft.Colors.WHITE,
            surface=ft.Colors.GREY_50,
            on_surface=ft.Colors.BLUE_GREY_900,
            outline=ft.Colors.BLUE_GREY_100,
            surface_container_highest=ft.Colors.WHITE,
        ),
        visual_density=ft.VisualDensity.COMFORTABLE,
        font_family="Inter",
    )
