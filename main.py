import random
from functools import partial
from pathlib import Path
from typing import List
from enum import Enum
import flet as ft

color_scheme = {
    'background': "#242933",
    'nav_background': '#1c232e',
    'primary': '#ed4c57',  # red
    'secondary': '#f5efe9',  # white
    'tertiary': '#5a6173',  # gray
}

FONT_SIZE = 25

LANGUAGE_TO_PATH = {
    'en': Path('./assets/vocabulary/en-1000.txt'),
    'ru': Path('./assets/vocabulary/ru-10000.txt')
}

ALLOWED_CHARS = ' abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя'

DEFAULT_WORDS_COUNT = [10, 25, 50, 100]
DEFAULT_TIMES = [15, 30, 60, 120]


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
            size=FONT_SIZE,
            color=self.color,
            font_family="RobotoMono",
        )


class MainText(ft.UserControl):
    def __init__(self, text: str, letter_colors: List[LetterColor] = None):
        super().__init__()
        self.text = text
        self.letter_colors = letter_colors if letter_colors is not None else [
            0] * len(text)

        self.content_container = ft.Container(self.generate_content())

        # assert len(text) == len(letter_state)

    def generate_content(self):
        """Returns content with self.text and self.letter_colors"""

        current_word_letters: List[Letter] = []
        completed_words = []
        for letter, color in zip(self.text, self.letter_colors):
            current_word_letters.append(Letter(letter, color))
            if letter == ' ':
                completed_words.append(
                    ft.Row(current_word_letters, spacing=0, run_spacing=0, wrap=True))
                current_word_letters = []

        if len(current_word_letters) != 0:
            completed_words.append(
                ft.Row(current_word_letters, spacing=0, run_spacing=0, wrap=True))

        return ft.Container(
            content=ft.Row(
                controls=completed_words,
                wrap=True,
                spacing=0,
                run_spacing=0
            ),
            alignment=ft.alignment.center,
            width=1000,
        )

    def update_content(self, letter_colors: List[LetterColor]):
        self.letter_colors = letter_colors

        self.content_container.content = self.generate_content()

        self.content_container.update()
        self.update()

    def build(self):
        return self.content_container


class Statistics:
    # TODO
    def __init__(self):
        pass


class TypingTest:
    def __init__(self, page: ft.Page):
        self.is_running = False
        self.statistics = Statistics()

        self.text_generator = TextGenerator(language='en')
        self.need_type = self.text_generator.generate(30)
        self.letter_color = [LetterColor.UNUSED] * len(self.need_type)

        self.printed_text = ""

        self.display_text = self.need_type

        self.main_text = MainText(text=self.display_text,
                                  letter_colors=self.letter_color)

        self.settings_bar = SettingsBar(typing_test=self)

        page.add(self.settings_bar)
        page.add(self.main_text)

    def start(self):
        # TODO, what it should do
        pass

    def toggle_punctuation(self):
        print('toggle punctuation')

    def toggle_numbers(self):
        print('toggle numbers')

    def select_time(self, count: int = 15):
        print('select time', count)

    def select_words(self, count: int = 25):
        print('select words', count)

    def key_pressed(self, e):
        """Handles user key press event"""

        key = e.key.lower()

        if key == 'backspace':
            idx = len(self.printed_text) - 1
            if idx >= 0 and (self.printed_text[idx] != ' '
                             or self.printed_text[idx] != self.need_type[idx]):

                self.printed_text = self.printed_text[:-1]
                self.letter_color[idx] = LetterColor.UNUSED

        elif key in ALLOWED_CHARS:
            position = len(self.printed_text)
            need_key = self.need_type[position]

            self.printed_text += key
            if need_key == key:
                self.letter_color[position] = LetterColor.CORRECT
            else:
                self.letter_color[position] = LetterColor.WRONG

        self.main_text.update_content(self.letter_color)


class SettingsBar(ft.UserControl):
    """Main typing test settings bar interface"""

    class LabeledButton(ft.UserControl):
        """One element of Settings bar"""

        def __init__(self, text: str, is_on: bool, on_click):
            super().__init__()

            self.text = text
            self.is_on = is_on
            self.container = ft.Container(
                self.generate_content(),
                on_click=on_click
            )
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

            new_color = color_scheme['primary'] if self.is_on else color_scheme['tertiary']
            self.container.content.color = new_color

        def generate_content(self) -> ft.UserControl:
            """Returns content for container"""
            color = color_scheme['primary'] if self.is_on else color_scheme['tertiary']

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

    def __init__(self, typing_test: TypingTest, words_selected: bool = True):
        self.typing_test = typing_test

        self.words_selected = words_selected

        self.punctuation = self.LabeledButton(
            "punctuation", is_on=False, on_click=self.toggle_punctuation)
        self.numbers = self.LabeledButton(
            "numbers", is_on=False, on_click=self.toggle_numbers)
        self.time = self.LabeledButton(
            "time", is_on=not words_selected, on_click=self.select_time)
        self.words = self.LabeledButton(
            "words", is_on=words_selected, on_click=self.select_words)

        self.buttons: List[ft.UserControl] = [
            self.LabeledButton("loading", False, None) for i in range(4)]
        self.selected_size_option = 1

        self.content = ft.Row([
            self.punctuation,
            self.numbers,
            ft.VerticalDivider(width=-3),
            self.time,
            self.words,
            ft.VerticalDivider(width=-3),
        ] + self.buttons, spacing=15, alignment=ft.MainAxisAlignment.CENTER)

        self.container = ft.Container(
            self.content,
            padding=10,
            border_radius=10,
            width=520,
            bgcolor=color_scheme['nav_background'],
            alignment=ft.alignment.center
        )

        self.update_buttons()

        super().__init__()

    def toggle_punctuation(self, _):
        """Updates punctuation button and redirects further"""
        self.typing_test.toggle_punctuation()

        self.punctuation.toggle()
        self.punctuation.update()

    def toggle_numbers(self, _):
        """Updates numbers button and redirects further"""
        self.typing_test.toggle_numbers()

        self.numbers.toggle()
        self.numbers.update()

    def select_time(self, _, button_idx: int = 1):
        self.words.toggle(False)
        self.time.toggle(True)

        self.words.update()
        self.time.update()

        self.words_selected = False
        self.selected_size_option = button_idx
        self.update_buttons()
        self.content.update()

        self.typing_test.select_time(button_idx)

    def select_words(self, _, button_idx: int = 1):
        self.words.toggle(True)
        self.time.toggle(False)

        self.words.update()
        self.time.update()

        self.words_selected = True
        self.selected_size_option = button_idx
        self.update_buttons()
        self.content.update()

        self.typing_test.select_words(button_idx)

    def update_buttons(self):
        """Returns content for container"""
        # new_buttons = [
        #     self.LabeledButton(
        #         DEFAULT_WORDS_COUNT[i] if self.words_selected else DEFAULT_TIMES[i],
        #         is_on=(i == self.selected_size_option),
        #         on_click=partial(
        #             self.select_words if self.words_selected else self.select_time, button_idx=i)
        #     )
        #     for i in range(4)
        # ]

        for i in range(4):
            print(self.words_selected)
            self.content.controls[-4 + i] = self.LabeledButton(
                DEFAULT_WORDS_COUNT[i] if self.words_selected else DEFAULT_TIMES[i],
                is_on=(i == self.selected_size_option),
                on_click=partial(
                    self.select_words if self.words_selected else self.select_time, button_idx=i)
            )
            # button.text = DEFAULT_WORDS_COUNT[i] if self.words_selected else DEFAULT_TIMES[i]
            # button.is_on = (i == self.selected_size_option)
            # button.on_click = partial(
            #     self.select_words if self.words_selected else self.select_time, button_idx=i)

            # if added_to_page:
            #     button.update()

    def build(self):
        print(self.container.content.controls[-3].text)
        return self.container


def main(page: ft.Page):
    page.title = "Typing app"
    page.window_width = 1200
    page.window_height = 700
    page.bgcolor = color_scheme['background']
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.fonts = {
        "RobotoMono": "./assets/RobotoMono-VariableFont_wght.ttf"
    }

    typing_test = TypingTest(page)

    page.on_keyboard_event = typing_test.key_pressed
    page.update()


ft.app(target=main)
