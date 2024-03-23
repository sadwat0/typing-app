import os
from csv import DictWriter
import random
import datetime
from functools import partial
from pathlib import Path
from typing import List
from enum import Enum
import pandas as pd
import flet as ft
from flet_timer.flet_timer import Timer


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

PUNCTUATION_CHARS = '.,;?!'
ALLOWED_CHARS = ' abcdefghijklmnopqrstuvwxyz' \
    + 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя' \
    + '0123456789' \
    + PUNCTUATION_CHARS

DEFAULT_WORDS_COUNT = [10, 25, 50, 100]
DEFAULT_TIMES = [10, 15, 30, 60]

STATISTICS_FIELD_NAMES = [
    'wpm', 'accuracy',
    'test_size_mode', 'test_size',
    'language',
    'punctuation', 'numbers',
    'total_key_presses', 'correct_key_presses',
    'start_time', 'end_time'
]

# Checking for saves file existence
if not os.path.exists('./saves'):
    os.makedirs('./saves')

if not os.path.isfile('./saves/data.csv'):
    with open('./saves/data.csv', 'w', encoding='utf-8') as f:
        f.write(",".join(STATISTICS_FIELD_NAMES) + '\n')


class TextGenerator:
    """Generates text according to settings"""

    def __init__(
        self,
        language: str = "en",
        vocabulary_path: str = None,
        punctuation: bool = False,
        numbers: bool = False,
    ):
        self.language = language
        self.vocabulary = ["empty"]
        self.punctuation = punctuation
        self.numbers = numbers

        if vocabulary_path is not None:
            self.load_vocabulary(vocabulary_path)
        elif language is not None:
            self.load_vocabulary(LANGUAGE_TO_PATH[language])

    def toggle_punctuation(self):
        """Toggles punctuation for generation"""
        self.punctuation = not self.punctuation

    def toggle_numbers(self):
        """Toggles numbers for generation"""
        self.numbers = not self.numbers

    def load_vocabulary(self, path: str):
        """Loads vocab from certain path"""
        with open(path, 'r', encoding='utf8') as vocabulary_file:
            self.vocabulary = [line[:-1]
                               for line in vocabulary_file.readlines()]

    def generate(self, words_count: int = 20) -> str:
        """Generates text to print according to settings."""
        words = []

        for _ in range(words_count):
            current_word = random.choice(self.vocabulary)

            # add numbers
            if self.numbers and random.uniform(0, 1) <= 0.15:
                current_word = str(random.randint(0, 10_000))

            # add punctuation
            if self.punctuation and random.uniform(0, 1) <= 0.15:
                current_word += random.choice(PUNCTUATION_CHARS)

            words.append(current_word)

        return " ".join(words)


class LetterColor(Enum):
    """Enum for color names"""

    CORRECT = color_scheme['secondary']
    WRONG = color_scheme['primary']
    UNUSED = color_scheme['tertiary']


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
        self.letter_colors = letter_colors if letter_colors is not None else [
            LetterColor.UNUSED] * len(text)

        self.content_container = ft.Container(self.generate_content())

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


class Statistics:
    """
    Stores information about running or completed test
    and calculates typing speed (cpm, wpm), accuracy
    """

    def __init__(
        self,
        test_size_mode: str | None = None,
        test_size: str | None = None,
        language: str | None = None,
        punctuation: bool = False,
        numbers: bool = False,
        start_time: datetime.datetime | None = None,
        end_time: datetime.datetime | None = None,
        total_key_presses: int = 0,
        correct_key_presses: int = 0
    ):
        self.test_size_mode = test_size_mode
        self.test_size = test_size
        self.language = language

        self.start_time = start_time
        if start_time is None:
            self.start_time = datetime.datetime.now()

        # if None it means, that test is not over yer
        self.end_time = end_time

        self.total_key_presses = total_key_presses
        self.correct_key_presses = correct_key_presses

        self.punctuation = punctuation
        self.numbers = numbers

    def key_pressed(self, key: str, is_correct: bool | None = None):
        """Handles key press

        Args:
            key (str): allowed char or backspace
            is_correct (bool | None, optional): Must be not None if key != backspace.
        """

        if key != 'backspace':
            self.total_key_presses += 1
            self.correct_key_presses += is_correct

    def get_accuracy(self) -> float:
        """Returns accuracy (in percents)"""

        if self.total_key_presses == 0:
            return 100.0
        return self.correct_key_presses / self.total_key_presses * 100.0

    def get_cpm(self) -> float:
        """Returns average cpm"""
        current_time = self.end_time
        if current_time is None:
            current_time = datetime.datetime.now()

        start_timestamp = self.start_time.timestamp()
        current_timestamp = current_time.timestamp()

        delta_minutes = (current_timestamp - start_timestamp) / 60.0

        if delta_minutes == 0:
            return 0.0

        return self.correct_key_presses / delta_minutes

    def get_wpm(self) -> float:
        """Returns average wpm (1 word == 5 chars)"""
        return self.get_cpm() / 5.0

    def end(self):
        """Writes end_time with current time"""
        self.end_time = datetime.datetime.now()

    def save(self):
        """Saves to file"""
        stats_dict = {
            'wpm': self.get_wpm(),
            'accuracy': self.get_accuracy(),
            'test_size_mode': self.test_size_mode,
            'test_size': self.test_size,
            'language': self.language,
            'punctuation': self.punctuation,
            'numbers': self.numbers,
            'total_key_presses': self.total_key_presses,
            'correct_key_presses': self.correct_key_presses,
            'start_time': self.start_time.strftime('%H:%M:%S.%f %d/%m/%y'),
            'end_time': self.end_time.strftime('%H:%M:%S.%f %d/%m/%y')
        }

        with open('./saves/data.csv', 'a', newline='', encoding='utf-8') as stats_file:
            DictWriter(stats_file, fieldnames=STATISTICS_FIELD_NAMES).writerow(
                stats_dict)

    def load(self, index: int):
        """Loads from """


class TypingTest:
    class TestStatus(Enum):
        """Enum for typing test status"""

        NOT_STARTED = 0
        RUNNING = 1
        ENDED = 2

    def __init__(self, page: ft.Page):
        self.status = self.TestStatus.NOT_STARTED
        self.page = page

        self.language = 'en'
        self.size_mode = 'words'
        # if not None (size_mode = time) means amount of seconds given for test
        self.available_time: int | None = None

        self.timer = None

        self.words_to_generate = DEFAULT_WORDS_COUNT[1]

        self.text_generator = TextGenerator(language=self.language)
        self.correct_text = self.text_generator.generate(
            self.words_to_generate)
        self.letter_colors = [LetterColor.UNUSED] * len(self.correct_text)
        self.display_text = self.correct_text

        self.printed_text = ""

        self.main_text = MainText(text=self.display_text,
                                  letter_colors=self.letter_colors)
        self.settings_bar = SettingsBar(typing_test=self)
        self.information_bar = InformationBar()
        self.statistics: Statistics = None

        self.can_type = True

        self.visual_element = ft.Column(
            [
                self.settings_bar,
                self.main_text
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )

    def start(self):
        """Initializes new test (after user pressed button)"""

        self.status = self.TestStatus.RUNNING
        self.statistics = Statistics(
            test_size_mode=self.size_mode,
            test_size=self.words_to_generate if self.size_mode == 'words' else
            self.available_time,
            language=self.language,
            punctuation=self.text_generator.punctuation,
            numbers=self.text_generator.numbers,
        )

        self.visual_element.controls[0] = self.information_bar
        self.visual_element.update()

        self.timer = Timer(name="timer", interval_s=1,
                           callback=self.every_second)
        self.page.views[-1].controls.append(self.timer)
        self.page.views[-1].update()

    def stop(self):
        """Ends test (when user typed everything or time run out)"""

        self.status = self.TestStatus.ENDED
        self.statistics.end()
        self.statistics.save()

        self.timer = None
        self.page.views[-1].controls.pop()
        self.page.views[-1].update()

        self.page.go("/stats")

    def restart(self):
        """
        Restart test
        WARNING: not save statistics if test is not over
        """

        self.status = self.TestStatus.NOT_STARTED
        self.statistics = None
        self.regenerate_text()
        self.printed_text = ""

        self.visual_element.controls[0] = self.settings_bar
        self.visual_element.update()

    def every_second(self):
        """Updates statistics and checks if test ended"""
        if self.status == self.TestStatus.RUNNING:
            self.update_information_bar()

            if self.size_mode == "time":
                current_time = datetime.datetime.now()
                delta = current_time - self.statistics.start_time

                if delta.total_seconds() >= self.available_time:
                    self.stop()

    def regenerate_text(self):
        """Updates text content according to settings"""

        self.correct_text = self.text_generator.generate(
            self.words_to_generate)
        self.letter_colors = [LetterColor.UNUSED] * len(self.correct_text)
        self.main_text.update_content(self.correct_text, self.letter_colors)

    def toggle_punctuation(self):
        """Changes punctuation setting"""

        # TODO: reset game
        self.text_generator.toggle_punctuation()
        self.regenerate_text()

    def toggle_numbers(self):
        """Changes numbers setting"""

        self.text_generator.toggle_numbers()
        self.regenerate_text()

    def select_time(self, count: int = 15):
        """Changes test mode to "time" and sets time to {count}"""
        self.size_mode = "time"
        self.available_time = count
        self.words_to_generate = 120

        self.regenerate_text()

    def select_words(self, count: int = 25):
        """Changes test mode to "words" and sets words count to {count}"""

        self.size_mode = "words"
        self.available_time = None
        self.words_to_generate = count

        self.regenerate_text()

    def update_information_bar(self):
        """Update wpm & accuracy text (during test)"""

        accuracy = self.statistics.get_accuracy()
        self.information_bar.set_accuracy(f"{accuracy:.1f}")

        wpm = self.statistics.get_wpm()
        self.information_bar.set_wpm(f"{wpm:.1f}")

    def key_pressed(self, e):
        """Handles user key press event"""

        if self.status == self.TestStatus.ENDED or not self.can_type:
            return

        key = e.key.lower()

        if self.status == self.TestStatus.NOT_STARTED and (key == 'backspace'
                                                           or key in ALLOWED_CHARS):
            self.start()

        if key == 'backspace':
            idx = len(self.printed_text) - 1
            if idx >= 0 and (self.printed_text[idx] != ' '
                             or self.printed_text[idx] != self.correct_text[idx]):

                self.printed_text = self.printed_text[:-1]
                self.letter_colors[idx] = LetterColor.UNUSED
                self.statistics.key_pressed(key)

        elif key in ALLOWED_CHARS:
            position = len(self.printed_text)
            need_key = self.correct_text[position]

            self.printed_text += key
            if need_key == key:
                self.letter_colors[position] = LetterColor.CORRECT
                self.statistics.key_pressed(key, is_correct=True)
            else:
                self.letter_colors[position] = LetterColor.WRONG
                self.statistics.key_pressed(key, is_correct=False)

        self.main_text.update_content(self.correct_text, self.letter_colors)
        self.update_information_bar()

        if len(self.correct_text) == len(self.printed_text):
            self.stop()


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

    def update_buttons(self):
        """Returns content for container"""

        for i in range(4):
            self.content.controls[-4 + i] = self.LabeledButton(
                DEFAULT_WORDS_COUNT[i] if self.words_selected else DEFAULT_TIMES[i],
                is_on=(i == self.selected_size_option),
                on_click=partial(
                    self.select_words if self.words_selected else self.select_time, button_idx=i)
            )

    def build(self):
        return self.container


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
        self.wpm = self.TextElement(
            value="000.0", color=color_scheme['primary'])
        self.accuracy = self.TextElement(
            value="100.0", color=color_scheme['primary'])

        self.content = ft.Row(
            [
                self.TextElement(
                    value="WPM:", color=color_scheme['tertiary']),
                self.wpm,
                ft.VerticalDivider(),
                self.TextElement(value="Accuracy:",
                                 color=color_scheme['tertiary']),
                self.accuracy
            ],
            spacing=15,
            alignment=ft.MainAxisAlignment.CENTER
        )

        self.container = ft.Container(
            self.content,
            padding=10,
            border_radius=10,
            width=520,
            bgcolor=color_scheme['nav_background'],
            alignment=ft.alignment.center
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


class StatisticsPage(ft.UserControl):
    """Graphical element for stats page"""

    class StatisticsVisualizer(ft.UserControl):
        """Graphical element for one test statistics"""

        def create_text_element(self, label: str, value: str) -> ft.Text:
            """Creates formated text graphical element"""

            return ft.Row(
                [
                    ft.Text(
                        f"{label}: ",
                        color=color_scheme['secondary'],
                        theme_style=ft.TextThemeStyle.TITLE_MEDIUM
                    ),
                    ft.Text(
                        value,
                        color=color_scheme['primary'],
                        theme_style=ft.TextThemeStyle.TITLE_MEDIUM
                    )
                ],
                width=170,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )

        def __init__(self, index: int, statistics: Statistics):
            super().__init__()

            self.statistics = statistics

            self.index = index
            self.text_stats = ft.Column(
                [
                    self.create_text_element(
                        "WPM", f"{self.statistics.get_wpm():.1f}"),
                    self.create_text_element(
                        "ACCURACY", f"{self.statistics.get_accuracy():.1f}%"),
                    self.create_text_element(
                        "LANGUAGE", f"{self.statistics.language}"),
                    self.create_text_element(
                        "MODE",
                        f"{self.statistics.test_size} words"
                        if self.statistics.test_size_mode == "words"
                        else f"{self.statistics.test_size}s"
                    ),
                    self.create_text_element(
                        "PUNCTUATION", "ON" if self.statistics.punctuation else "OFF"),
                    self.create_text_element(
                        "NUMBERS", "ON" if self.statistics.punctuation else "OFF"),
                    self.create_text_element(
                        "KEY PRESSES",
                        str(self.statistics.correct_key_presses) +
                        "/" +
                        str(self.statistics.total_key_presses)),
                    self.create_text_element(
                        "START", f"{self.statistics.start_time.strftime('%H:%M:%S')}"),
                    self.create_text_element(
                        "END", f"{self.statistics.end_time.strftime('%H:%M:%S')}"),
                ],
                spacing=2,
            )

        def build(self):
            return ft.Container(
                ft.Column(
                    [
                        ft.Text(
                            f"TEST #{self.index + 1}",
                            color=color_scheme['secondary'],
                            theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM
                        ),
                        ft.Row(
                            [
                                self.text_stats
                                # TODO: heatmap
                            ]
                        )
                    ]
                ),
                padding=20,
                border_radius=10,
                width=800,
                bgcolor=color_scheme['nav_background']
            )

    def __init__(self):
        super().__init__()

        self.list_content = []

        self.stats = pd.read_csv('./saves/data.csv')
        if len(self.stats) == 0:
            self.list_content = [
                ft.Text("You haven't passed any tests yet",
                        color=color_scheme['secondary'],
                        theme_style=ft.TextThemeStyle.HEADLINE_LARGE)
            ]
        else:
            for index, row in self.stats.iloc[::-1].iterrows():
                statistics_object = Statistics(
                    test_size_mode=row['test_size_mode'],
                    test_size=row['test_size'],
                    language=row['language'],
                    punctuation=row['punctuation'],
                    numbers=row['numbers'],
                    start_time=datetime.datetime.strptime(
                        row['start_time'], '%H:%M:%S.%f %d/%m/%y'),
                    end_time=datetime.datetime.strptime(
                        row['end_time'], '%H:%M:%S.%f %d/%m/%y'),
                    total_key_presses=row['total_key_presses'],
                    correct_key_presses=row['correct_key_presses']
                )

                self.list_content.append(
                    self.StatisticsVisualizer(index, statistics_object))

    def build(self):
        return ft.ListView(
            self.list_content,
            expand=1,
            spacing=10,
            auto_scroll=False
        )


def main(page: ft.Page):
    """Main function, start application"""

    page.title = "Typing app"
    page.window_width = 1200
    page.window_height = 700
    page.bgcolor = color_scheme['background']

    page.fonts = {
        "RobotoMono": "./assets/RobotoMono-VariableFont_wght.ttf"
    }

    typing_test = TypingTest(page)

    def route_change(_):
        page.views.clear()

        if page.route == '/':
            page.views.append(
                ft.View(
                    '/',
                    [
                        ft.ElevatedButton(
                            "View stats", on_click=lambda _: page.go("/stats")),
                        ft.Divider(),
                        typing_test.visual_element,
                    ],
                    bgcolor=color_scheme['background'],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )

            typing_test.can_type = True
        elif page.route == '/stats':
            list_view_builder = StatisticsPage()

            page.views.append(
                ft.View(
                    '/stats',
                    [
                        ft.ElevatedButton(
                            "Main Page", on_click=lambda _: page.go("/")),
                        ft.Divider(),
                        list_view_builder.build()
                    ],
                    bgcolor=color_scheme['background'],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )

            typing_test.can_type = False

        page.update()

        if page.route == '/':
            typing_test.restart()

    page.on_route_change = route_change
    page.go(page.route)

    page.on_keyboard_event = typing_test.key_pressed
    page.update()


ft.app(target=main)
