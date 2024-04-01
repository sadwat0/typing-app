"""Realizes TextGenerator"""

import random
from src.constants import LANGUAGE_TO_PATH, PUNCTUATION_CHARS


class TextGenerator:
    """Generates text according to settings"""

    def __init__(
        self,
        language: str = "en",
        punctuation: bool = False,
        numbers: bool = False,
    ):
        self.language = language
        self.vocabulary = ["empty"]
        self.punctuation = punctuation
        self.numbers = numbers

        self.load_vocabulary(LANGUAGE_TO_PATH[language])

    def toggle_punctuation(self):
        """Toggles punctuation for generation"""
        self.punctuation = not self.punctuation

    def toggle_numbers(self):
        """Toggles numbers for generation"""
        self.numbers = not self.numbers

    def set_language(self, language: str):
        """Update language"""

        self.language = language
        self.load_vocabulary(LANGUAGE_TO_PATH[language])

    def load_vocabulary(self, path: str):
        """Loads vocab from certain path"""
        with open(path, "r", encoding="utf8") as vocabulary_file:
            self.vocabulary = [line[:-1] for line in vocabulary_file.readlines()]

    def generate(self, words_count: int = 20) -> str:
        """Generates text to print according to settings."""
        words = []

        for _ in range(words_count):
            current_word = random.choice(self.vocabulary).lower()

            # add numbers
            if self.numbers and random.uniform(0, 1) <= 0.15:
                current_word = str(random.randint(0, 10_000))

            # add punctuation
            if self.punctuation and random.uniform(0, 1) <= 0.15:
                current_word += random.choice(PUNCTUATION_CHARS)

            words.append(current_word)

        return " ".join(words)
