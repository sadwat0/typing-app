"""MainText and needed for it classes"""

from enum import Enum
from typing import List
import flet as ft
from src.constants import FONT_SIZE


color_scheme = {
    "background": "#242933",
    "nav_background": "#1c232e",
    "primary": "#ed4c57",  # red
    "secondary": "#f5efe9",  # white
    "tertiary": "#5a6173",  # gray
}
# TODO: remove


class LetterColor(Enum):
    """Enum for color names"""

    CORRECT = color_scheme["secondary"]
    WRONG = color_scheme["primary"]
    UNUSED = color_scheme["tertiary"]


class Letter(ft.UserControl):
    """One letter from MainText"""

    def __init__(self, value: str, color: LetterColor):
        super().__init__()
        self.value = value
        self.color = color.value

    def build(self):
        return ft.Text(
            self.value,
            size=FONT_SIZE,
            color=self.color,
            font_family="RobotoMono",
        )


class MainText(ft.UserControl):
    """Graphic element for displaying typing test text"""

    def __init__(self, text: str, letter_colors: List[LetterColor] = None):
        super().__init__()
        self.text = text
        self.letter_colors = (
            letter_colors
            if letter_colors is not None
            else [LetterColor.UNUSED] * len(text)
        )

        self.content_container = ft.Container(self.generate_content())

    def generate_content(self):
        """Returns content with self.text and self.letter_colors"""

        current_word_letters: List[Letter] = []
        completed_words = []

        for letter, color in zip(self.text, self.letter_colors):
            current_word_letters.append(Letter(letter, color))
            if letter == " ":
                completed_words.append(
                    ft.Row(current_word_letters, spacing=0, run_spacing=0, wrap=True)
                )
                current_word_letters = []

        if len(current_word_letters) != 0:
            completed_words.append(
                ft.Row(current_word_letters, spacing=0, run_spacing=0, wrap=True)
            )

        return ft.Container(
            content=ft.Row(
                controls=completed_words, wrap=True, spacing=0, run_spacing=0
            ),
            alignment=ft.alignment.center,
            width=1000,
        )

    def update_content(self, text: str, letter_colors: List[LetterColor] | None = None):
        """Updates gui with new text

        Args:
            text (str): text to visualize
            letter_colors (List[LetterColor] | None):
                if None it equivalent to List[LetterColor.UNUSED]
        """

        if letter_colors is None:
            letter_colors = [LetterColor.UNUSED] * len(self.text)

        self.text = text
        self.letter_colors = letter_colors

        self.content_container.content = self.generate_content()

        self.content_container.update()
        self.update()

    def build(self):
        return self.content_container
