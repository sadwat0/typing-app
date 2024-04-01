"""Realizes Typing test class"""

import datetime
from enum import Enum
from flet_timer.flet_timer import Timer
import flet as ft

from .constants import DEFAULT_WORDS_COUNT, ALLOWED_CHARS
from .text_generator import TextGenerator
from .settings_bar import SettingsBar
from .information_bar import InformationBar
from .statistics_classes import Statistics, HeatmapStatistics
from .text_visualizing import MainText, LetterColor


class TypingTest:
    """Controls everything and redirects commands between different classes"""

    class TestStatus(Enum):
        """Enum for typing test status"""

        NOT_STARTED = 0
        RUNNING = 1
        ENDED = 2

    def __init__(self, page: ft.Page):
        self.status = self.TestStatus.NOT_STARTED
        self.page = page

        self.language = "en"
        self.size_mode = "words"
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

        self.main_text = MainText(
            text=self.display_text, letter_colors=self.letter_colors
        )
        self.settings_bar = SettingsBar(typing_test=self)
        self.information_bar = InformationBar()
        self.statistics: Statistics = None
        self.heatmap = HeatmapStatistics()

        self.can_type = True

        self.visual_element = ft.Column(
            [self.settings_bar, self.main_text],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def start(self):
        """Initializes new test (after user pressed button)"""

        self.status = self.TestStatus.RUNNING
        self.statistics = Statistics(
            test_size_mode=self.size_mode,
            test_size=(
                self.words_to_generate
                if self.size_mode == "words"
                else self.available_time
            ),
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
        self.heatmap.save()

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

        if self.status == self.TestStatus.NOT_STARTED and (
            key == "backspace" or key in ALLOWED_CHARS
        ):
            self.start()

        if key == "backspace":
            idx = len(self.printed_text) - 1
            if idx >= 0 and (
                self.printed_text[idx] != " "
                or self.printed_text[idx] != self.correct_text[idx]
            ):

                self.printed_text = self.printed_text[:-1]
                self.letter_colors[idx] = LetterColor.UNUSED
                self.statistics.key_pressed(key)

        elif key in ALLOWED_CHARS:
            position = len(self.printed_text)
            need_key = self.correct_text[position]

            self.heatmap.add_key_press(need_type=need_key, typed=key)

            self.printed_text += key
            if need_key == key:
                self.letter_colors[position] = LetterColor.CORRECT
                self.statistics.key_pressed(key, is_correct=True)
            else:
                self.letter_colors[position] = LetterColor.WRONG
                self.statistics.key_pressed(key, is_correct=False)

        self.main_text.update_content(self.correct_text, self.letter_colors)

        if self.status == self.TestStatus.RUNNING:
            self.update_information_bar()

        if len(self.correct_text) == len(self.printed_text):
            self.stop()
