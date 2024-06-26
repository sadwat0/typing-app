"""List of constants"""

from pathlib import Path
import flet as ft

color_scheme = {
    "background": "#242933",
    "nav_background": "#1c232e",
    "primary": "#ed4c57",  # red
    "secondary": "#f5efe9",  # white
    "tertiary": "#5a6173",  # gray
}

FONT_SIZE = 25

LANGUAGE_TO_PATH = {
    "en": Path("./assets/vocabulary/en-1000.txt"),
    "ru": Path("./assets/vocabulary/ru-10000.txt"),
}
LANGUAGE_LETTERS = {
    "en": "abcdefghijklmnopqrstuvwxyz",
    "ru": "абвгдеёжзийклмнопрстуфхцчшщъыьэюя",
}

PUNCTUATION_CHARS = ".,;?!"
DIGITS = "0123456789"
ALLOWED_CHARS = (
    " " + LANGUAGE_LETTERS["en"] + LANGUAGE_LETTERS["ru"] + DIGITS + PUNCTUATION_CHARS
)

DEFAULT_WORDS_COUNT = [10, 25, 50, 100]
DEFAULT_TIMES = [10, 15, 30, 60]

STATISTICS_FIELD_NAMES = [
    "wpm",
    "accuracy",
    "test_size_mode",
    "test_size",
    "language",
    "punctuation",
    "numbers",
    "total_key_presses",
    "correct_key_presses",
    "start_time",
    "end_time",
]

# flet not supports russian letters in keypress
QWERTY_NOT_RU_CHARS = "qwertyuiop[]asdfghjkl;'zxcvbnm,."
QWERTY_RU_CHARS = "йцукенгшщзхъфывапролджэячсмитьбю"

DOWNLOAD_URLS = {
    "custom_font": "https://drive.usercontent.google.com/download?id=18YoEbnanfCJ-oh8iN4wZkEiNQuyrNzt6&export=download&authuser=0",
    "language_en": "https://gist.githubusercontent.com/deekayen/4148741/raw/98d35708fa344717d8eee15d11987de6c8e26d7d/1-1000.txt",
    "language_ru": "https://raw.githubusercontent.com/hingston/russian/master/10000-russian-words-cyrillic-only.txt",
}

FILE_NAMES = {
    "custom_font": "RobotoMono-VariableFont_wght.ttf",
    "language_en": "en-1000.txt",
    "language_ru": "ru-10000.txt",
    "data": "data.csv",
    "heatmap": "heatmap.csv",
}

TYPING_TEST_DEFAULT_WORDS_ON_TIME = 120

DATE_FORMATS = {
    "test_start_end_time": "%H:%M:%S.%f %d/%m/%y",
    "stats_start_end_time": "%H:%M:%S",
}

MAIN_TEXT_WIDTH = 1000
HEATMAP = {
    "size": 500,
    "border_radius": 20,
    "padding": ft.padding.only(top=10, bottom=10, right=20),
}

SETTINGS_BAR = {"spacing": 15, "padding": 10, "border_radius": 10, "width": 600}

STATISTICS_PAGE = {
    "test_content_width": 170,
    "text_stats_spacing": 2,
    "test_padding": 20,
    "test_border_radius": 10,
    "test_width": 800,
    "spacing": 10,
}

TEXT_GENERATOR = {
    "numbers_probability": 0.15,
    "max_number": 10_000,
    "punctuation_probability": 0.15,
}

SETTINGS_BAR_DIVIDER_WIDTH = -3

MAX_ACCURACY = 100.0
CHARACTERS_IN_WORD = 5.0
SECONDS_IN_MINUTE = 60.0
DEFAULT_CPM_WITH_NO_TIME = 0.0
