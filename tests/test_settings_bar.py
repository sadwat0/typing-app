import pytest
from src.settings_bar import SettingsBar
from src.constants import DEFAULT_TIMES, DEFAULT_WORDS_COUNT
from src.typing_test import TypingTest
from src.utils import load_assets


def setup():
    load_assets()


@pytest.fixture
def typing_test_mock(monkeypatch):
    load_assets()

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


def test_toggle_punctuation(typing_test_mock):
    settings_bar = SettingsBar(typing_test_mock)
    assert not typing_test_mock.text_generator.punctuation
    settings_bar.toggle_punctuation(None)
    assert typing_test_mock.text_generator.punctuation


def test_toggle_numbers(typing_test_mock):
    settings_bar = SettingsBar(typing_test_mock)
    assert not typing_test_mock.text_generator.numbers
    settings_bar.toggle_numbers(None)
    assert typing_test_mock.text_generator.numbers


def test_select_time(typing_test_mock):
    settings_bar = SettingsBar(typing_test_mock)
    settings_bar.select_time(None, button_idx=2)
    assert typing_test_mock.size_mode == "time"
    assert typing_test_mock.available_time == DEFAULT_TIMES[2]


def test_select_words(typing_test_mock):
    settings_bar = SettingsBar(typing_test_mock)
    settings_bar.select_words(None, button_idx=3)
    assert typing_test_mock.size_mode == "words"
    assert typing_test_mock.available_time is None
    assert typing_test_mock.words_to_generate == DEFAULT_WORDS_COUNT[3]


def test_change_language(typing_test_mock):
    settings_bar = SettingsBar(typing_test_mock)
    assert typing_test_mock.language == "en"
    settings_bar.change_language(None)
    assert typing_test_mock.language == "ru"
    settings_bar.change_language(None)
    assert typing_test_mock.language == "en"
