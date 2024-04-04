import pytest
import flet as ft
from unittest.mock import patch
from src.typing_test import TypingTest, LetterColor


@pytest.fixture
def typing_test_mock(monkeypatch):
    class MockControl:
        def __init__(self):
            self.controls = []

        def update(self):
            pass

    class MockPage:
        """A mock implementation of the flet.Page class for testing purposes."""

        def __init__(self):
            self.views = [MockControl() for _ in range(5)]

        def go(self, path):
            pass

    def mock_update(_):
        pass

    monkeypatch.setattr("flet.Control.update", mock_update)
    page = MockPage()
    typing_test = TypingTest(page)

    return typing_test


def test_stop(typing_test_mock):
    typing_test_mock.start()
    typing_test_mock.stop()
    assert typing_test_mock.status == typing_test_mock.TestStatus.ENDED


def test_settings_changes(typing_test_mock):
    old_punctuation = typing_test_mock.text_generator.punctuation
    typing_test_mock.toggle_punctuation()
    assert typing_test_mock.text_generator.punctuation != old_punctuation

    old_numbers = typing_test_mock.text_generator.numbers
    typing_test_mock.toggle_numbers()
    assert typing_test_mock.text_generator.numbers != old_numbers

    typing_test_mock.select_time()
    assert typing_test_mock.size_mode == "time"
    assert typing_test_mock.available_time > 0

    typing_test_mock.select_words()
    assert typing_test_mock.size_mode == "words"
    assert typing_test_mock.available_time is None

    typing_test_mock.set_language(language="ru")
    assert typing_test_mock.language == "ru"


def test_key_pressed_starts_test(typing_test_mock):
    assert typing_test_mock.status == TypingTest.TestStatus.NOT_STARTED

    event = ft.KeyboardEvent("a", False, False, False, False)
    typing_test_mock.key_pressed(event)

    assert typing_test_mock.status == TypingTest.TestStatus.RUNNING


def test_key_pressed_correct_key(typing_test_mock):
    typing_test_mock.correct_text = "hello"
    typing_test_mock.printed_text = "he"

    event = ft.KeyboardEvent("l", False, False, False, False)
    typing_test_mock.key_pressed(event)

    assert typing_test_mock.printed_text == "hel"
    assert typing_test_mock.letter_colors[2] == LetterColor.CORRECT


def test_key_pressed_wrong_key(typing_test_mock):
    typing_test_mock.correct_text = "hello"
    typing_test_mock.printed_text = "he"

    event = ft.KeyboardEvent("a", False, False, False, False)
    typing_test_mock.key_pressed(event)

    assert typing_test_mock.printed_text == "hea"
    assert typing_test_mock.letter_colors[2] == LetterColor.WRONG


def test_backspace_pressed(typing_test_mock):
    typing_test_mock.correct_text = "hello"
    typing_test_mock.printed_text = "hea"

    event = ft.KeyboardEvent("backspace", False, False, False, False)
    typing_test_mock.key_pressed(event)

    assert typing_test_mock.printed_text == "he"
    assert typing_test_mock.letter_colors[2] == LetterColor.UNUSED
