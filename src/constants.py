"""List of constants"""

from pathlib import Path

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
