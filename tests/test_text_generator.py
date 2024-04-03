import re
import random
import pytest
from src.text_generator import TextGenerator
from src import constants


@pytest.fixture(scope="module")
def text_generator_setup(request):
    return TextGenerator(language="en")


def test_no_numbers(text_generator_setup):
    assert text_generator_setup.numbers is False

    generated_text = text_generator_setup.generate(words_count=1000)

    # check if no numbers in string
    assert bool(re.search(r"\d", generated_text)) is False


def test_numbers(text_generator_setup):
    random.seed(42)
    if text_generator_setup.numbers is False:
        text_generator_setup.toggle_numbers()

    generated_text = text_generator_setup.generate(100)
    assert len(set(constants.DIGITS) & set(generated_text)) > 0


def test_no_punctuation(text_generator_setup):
    assert text_generator_setup.punctuation is False

    generated_text = text_generator_setup.generate(words_count=1000)
    # check if no numbers in string
    assert bool(re.search(r"[.,;?!]", generated_text)) is False


def test_punctuation(text_generator_setup):
    random.seed(42)
    if text_generator_setup.punctuation is False:
        text_generator_setup.toggle_punctuation()

    generated_text = text_generator_setup.generate(100)
    assert len(set(constants.PUNCTUATION_CHARS) & set(generated_text)) > 0


def test_language(text_generator_setup):
    for language in ["ru", "en"]:
        other_language = "ru" if language == "en" else "en"

        text_generator_setup.set_language(language)

        generated_text = text_generator_setup.generate(100)
        for letter in generated_text:
            assert letter not in constants.LANGUAGE_LETTERS[other_language]
