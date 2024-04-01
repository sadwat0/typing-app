"""Reliaes information bar graphical element"""

import flet as ft

color_scheme = {
    "background": "#242933",
    "nav_background": "#1c232e",
    "primary": "#ed4c57",  # red
    "secondary": "#f5efe9",  # white
    "tertiary": "#5a6173",  # gray
}


class InformationBar(ft.UserControl):
    """Visualizes information during test"""

    class TextElement(ft.UserControl):
        """One of information bar elements"""

        def __init__(self, value: str, color):
            super().__init__()
            self.value = value
            self.color = color

            self.element = ft.Text(
                self.value,
                theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                font_family="RobotoMono",
                color=self.color,
            )

        def build(self):
            return self.element

    def __init__(self):
        self.wpm = self.TextElement(value="000.0", color=color_scheme["primary"])
        self.accuracy = self.TextElement(value="100.0", color=color_scheme["primary"])

        self.content = ft.Row(
            [
                self.TextElement(value="WPM:", color=color_scheme["tertiary"]),
                self.wpm,
                ft.VerticalDivider(),
                self.TextElement(value="Accuracy:", color=color_scheme["tertiary"]),
                self.accuracy,
            ],
            spacing=15,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        self.container = ft.Container(
            self.content,
            padding=10,
            border_radius=10,
            width=520,
            bgcolor=color_scheme["nav_background"],
            alignment=ft.alignment.center,
        )

        super().__init__()

    def set_wpm(self, value: str):
        """Update displayed accuracy information"""
        self.wpm.element.value = value
        self.wpm.update()

    def set_accuracy(self, value: str):
        """Update displayed accuracy information"""
        self.accuracy.element.value = f"{value}%"
        self.accuracy.update()

    def build(self):
        return self.container
