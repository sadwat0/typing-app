"""Realizes settings bar graphical element"""

from typing import List
from functools import partial
import flet as ft
from src.constants import DEFAULT_TIMES, DEFAULT_WORDS_COUNT

color_scheme = {
    "background": "#242933",
    "nav_background": "#1c232e",
    "primary": "#ed4c57",  # red
    "secondary": "#f5efe9",  # white
    "tertiary": "#5a6173",  # gray
}


class SettingsBar(ft.UserControl):
    """Main typing test settings bar interface"""

    class LabeledButton(ft.UserControl):
        """One element of Settings bar"""

        def __init__(self, text: str, is_on: bool, on_click):
            super().__init__()

            self.text = text
            self.is_on = is_on
            self.container = ft.Container(self.generate_content(), on_click=on_click)
            self.on_click = on_click

        def toggle(self, is_on: bool | None = None):
            """Updates color of button

            Args:
                is_on (bool | None): change to is_on if set, else toggle
            """

            if is_on is None:
                self.is_on = not self.is_on
            else:
                self.is_on = is_on

            new_color = (
                color_scheme["primary"] if self.is_on else color_scheme["tertiary"]
            )
            self.container.content.color = new_color

        def generate_content(self) -> ft.UserControl:
            """Returns content for container"""
            color = color_scheme["primary"] if self.is_on else color_scheme["tertiary"]

            return ft.Text(
                self.text,
                theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                font_family="RobotoMono",
                color=color,
            )

        def update(self):
            self.container.content = self.generate_content()
            super().update()

        def build(self):
            return self.container

    def __init__(self, typing_test, language: str = "en", words_selected: bool = True):
        self.typing_test = typing_test

        self.words_selected = words_selected

        self.language = language
        self.language_button = self.LabeledButton(
            self.language, is_on=True, on_click=self.change_language
        )

        self.punctuation = self.LabeledButton(
            "punctuation", is_on=False, on_click=self.toggle_punctuation
        )
        self.numbers = self.LabeledButton(
            "numbers", is_on=False, on_click=self.toggle_numbers
        )
        self.time = self.LabeledButton(
            "time", is_on=not words_selected, on_click=self.select_time
        )
        self.words = self.LabeledButton(
            "words", is_on=words_selected, on_click=self.select_words
        )

        self.buttons: List[ft.UserControl] = [
            self.LabeledButton("loading", False, None) for i in range(4)
        ]
        self.selected_size_option = 1

        self.content = ft.Row(
            [
                self.language_button,
                ft.VerticalDivider(width=-3),
                self.punctuation,
                self.numbers,
                ft.VerticalDivider(width=-3),
                self.time,
                self.words,
                ft.VerticalDivider(width=-3),
            ]
            + self.buttons,
            spacing=15,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        self.container = ft.Container(
            self.content,
            padding=10,
            border_radius=10,
            width=600,
            bgcolor=color_scheme["nav_background"],
            alignment=ft.alignment.center,
        )

        self.update_buttons()

        super().__init__()

    def toggle_punctuation(self, _):
        """Toggles punctuation setting"""
        self.typing_test.toggle_punctuation()

        self.punctuation.toggle()
        self.punctuation.update()

    def toggle_numbers(self, _):
        """Toggles numbers settings"""
        self.typing_test.toggle_numbers()

        self.numbers.toggle()
        self.numbers.update()

    def select_time(self, _, button_idx: int = 1):
        """Updates mode and text length"""

        self.words.toggle(False)
        self.time.toggle(True)

        self.words.update()
        self.time.update()

        self.words_selected = False
        self.selected_size_option = button_idx
        self.update_buttons()
        self.content.update()

        self.typing_test.select_time(DEFAULT_TIMES[button_idx])

    def select_words(self, _, button_idx: int = 1):
        """Updates mode and text length"""

        self.words.toggle(True)
        self.time.toggle(False)

        self.words.update()
        self.time.update()

        self.words_selected = True
        self.selected_size_option = button_idx
        self.update_buttons()
        self.content.update()

        self.typing_test.select_words(DEFAULT_WORDS_COUNT[button_idx])

    def change_language(self, _):
        """Switch language 'en' <-> 'ru'"""

        new_language = "ru" if self.language == "en" else "en"
        self.language_button.text = new_language
        self.language_button.update()

        self.language = new_language
        self.typing_test.set_language(new_language)

    def update_buttons(self):
        """Returns content for container"""

        for i in range(4):
            self.content.controls[-4 + i] = self.LabeledButton(
                DEFAULT_WORDS_COUNT[i] if self.words_selected else DEFAULT_TIMES[i],
                is_on=(i == self.selected_size_option),
                on_click=partial(
                    self.select_words if self.words_selected else self.select_time,
                    button_idx=i,
                ),
            )

    def build(self):
        return self.container
