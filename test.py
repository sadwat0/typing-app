import string
import random
from pathlib import Path
from typing import List
from enum import Enum
import flet as ft

color_scheme = {
    'background': "#242933",
    'primary': '#ed4c57',  # red
    'secondary': '#f5efe9',  # white
    'tertiary': '#5a6173',  # gray
}

LANGUAGE_TO_PATH = {
    'en': Path('./assets/vocabulary/en-1000.txt'),
    'ru': Path('./assets/vocabulary/ru-10000.txt')
}

ALLOWED_CHARS = ' abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя'


class TextGenerator:
    def __init__(
        self,
        language: str = "en",
        vocabulary_path: str = None
    ):
        self.language = language
        self.vocabulary = ["empty"]

        if vocabulary_path is not None:
            self.load_vocabulary(vocabulary_path)
        elif language is not None:
            self.load_vocabulary(LANGUAGE_TO_PATH[language])

    def load_vocabulary(self, path: str):
        """Loads vocab from certain path"""
        with open(path, 'r', encoding='utf8') as f:
            self.vocabulary = [line[:-1] for line in f.readlines()]

    def generate(self, words_count: int = 20) -> str:
        """Generates text to print according to settings."""
        return " ".join(random.sample(self.vocabulary, words_count))


t = TextGenerator(language='en')
print(t.generate(10))


class LetterColor(Enum):
    CORRECT = color_scheme['secondary']
    WRONG = color_scheme['primary']
    UNUSED = color_scheme['tertiary']


class Letter(ft.UserControl):
    def __init__(self, content: str, color: LetterColor):
        super().__init__()
        self.content = content
        self.color = color.value

    def build(self):
        return ft.Text(
            self.content,
            size=30,
            color=self.color,
            font_family="RobotoMono",
        )


class MainText(ft.UserControl):
    def __init__(self, text: str, letter_colors: List[LetterColor] = None):
        super().__init__()
        self.text = text
        self.letter_colors = letter_colors if letter_colors is not None else [
            0] * len(text)
        
        self.content = ft.Container(
            content=ft.Row(
                controls=[
                    Letter(letter, color) for letter, color in
                    zip(self.text, self.letter_colors)
                    # ] + [self.pipe],
                ],
                wrap=True,
                spacing=1,
            ),
            alignment=ft.alignment.center,
            animate=ft.animation.Animation(500, "bounceOut")
        )

        self.content_container = ft.AnimatedSwitcher(
            self.content,
            transition=ft.AnimatedSwitcherTransition.FADE,
            duration=100,
            reverse_duration=100,
        )

        # assert len(text) == len(letter_state)

        # self.pipe = ft.Container(
        #     width=2,
        #     height=32,
        #     bgcolor=color_scheme['primary'],
        #     animate=ft.animation.Animation(300)
        # )

    # def animate_pipe(self, e):
    #     # TODO
    #     self.pipe.bgcolor = color_scheme['tertiary'] if self.pipe.bgcolor == color_scheme['primary'] else color_scheme['primary']
    #     self.pipe.update()
    #     self.update()

    def update_content(self, letter_colors: List[LetterColor]):
        self.letter_colors = letter_colors
        
        # self.content = 

        self.content_container.content = ft.Row(
            controls=[
                Letter(letter, color) for letter, color in
                zip(self.text, self.letter_colors)
                # ] + [self.pipe],
            ],
            wrap=True,
            spacing=1,
        )
        
        self.content_container.update()
        self.update()

    def build(self):
        return self.content_container


class Statistics:
    def __init__(self):
        pass


class TypingTest:
    def __init__(self, page: ft.Page):
        self.is_running = False
        self.statistics = Statistics()

        self.text_generator = TextGenerator(language='en')
        self.need_type = self.text_generator.generate(30)
        self.current_status = [LetterColor.UNUSED] * len(self.need_type)

        self.printed_text = ""

        self.display_text = self.need_type

        self.main_text = MainText(text=self.display_text,
                                  letter_colors=self.current_status)

        page.add(self.main_text)

    def key_pressed(self, e):
        """Handles user key press event"""
        key = e.key.lower()
        if key == 'backspace':
            print('backspace, TODO')
        elif key in ALLOWED_CHARS:
            position = len(self.printed_text)
            need_key = self.need_type[position]

            self.printed_text += key
            if need_key == key:
                self.current_status[position] = LetterColor.CORRECT
            else:
                self.current_status[position] = LetterColor.WRONG

            self.main_text.update_content(self.current_status)


def main(page: ft.Page):
    page.title = "Typing app"
    page.window_width = 1200
    page.window_height = 700
    page.bgcolor = color_scheme['background']

    page.fonts = {
        "RobotoMono": "./assets/RobotoMono-VariableFont_wght.ttf"
    }

    typing_test = TypingTest(page)

    page.on_keyboard_event = typing_test.key_pressed
    page.update()


ft.app(target=main)
