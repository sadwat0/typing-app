# import re
# import random
# import pytest
# from src.text_generator import TextGenerator
# from src.typing_test import TypingTest, LetterColor
# from src import constants
# from src.statistics_classes import Statistics
# import sys
# import copy
# import flet as ft


# def fill_page_content(page: ft.Page, typing_test: TypingTest):
#     """Adds some elements to page for default work of typing test"""

#     page.views.append(
#         ft.View(
#             "/",
#             [
#                 ft.Row(
#                     [
#                         ft.ElevatedButton(
#                             "Statistics", on_click=lambda _: page.go("/stats")
#                         ),
#                         ft.ElevatedButton(
#                             "Heatmaps", on_click=lambda _: page.go("/heatmaps")
#                         ),
#                     ],
#                     alignment=ft.MainAxisAlignment.CENTER,
#                 ),
#                 ft.Divider(),
#                 typing_test.visual_element,
#             ],
#             bgcolor=constants.color_scheme["background"],
#             horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#         )
#     )
#     page.update()


# def get_typing_test(page: ft.Page) -> TypingTest:
#     typing_test = TypingTest(page)
#     fill_page_content(page, typing_test)

#     return typing_test


# def test_stop():
#     def test(page: ft.Page):
#         typing_test = get_typing_test(page)

#         # Test begin
#         typing_test.start()
#         typing_test.stop()
#         assert typing_test.status == typing_test.TestStatus.ENDED

#         page.window_destroy()

#     ft.app(target=test)


# def test_settings_changes():
#     def test(page: ft.Page):
#         typing_test = get_typing_test(page)

#         # Test begin
#         old_punctuation = typing_test.text_generator.punctuation
#         typing_test.toggle_punctuation()
#         assert typing_test.text_generator.punctuation != old_punctuation

#         old_numbers = typing_test.text_generator.numbers
#         typing_test.toggle_numbers()
#         assert typing_test.text_generator.numbers != old_numbers

#         typing_test.select_time()
#         assert typing_test.size_mode == "time"
#         assert typing_test.available_time > 0

#         typing_test.select_words()
#         assert typing_test.size_mode == "words"
#         assert typing_test.available_time is None

#         typing_test.set_language(language="ru")
#         assert typing_test.language == "ru"

#         page.window_destroy()

#     ft.app(target=test)


# def test_key_pressed_starts_test():
#     def test(page: ft.Page):
#         typing_test = get_typing_test(page)

#         # Test begin
#         assert typing_test.status == TypingTest.TestStatus.NOT_STARTED

#         event = ft.KeyboardEvent("a", False, False, False, False)
#         typing_test.key_pressed(event)

#         assert typing_test.status == TypingTest.TestStatus.RUNNING

#         page.window_destroy()

#     ft.app(target=test)


# def test_key_pressed_correct_key():
#     def test(page: ft.Page):
#         typing_test = get_typing_test(page)

#         # Test begin
#         typing_test.correct_text = "hello"
#         typing_test.printed_text = "he"

#         event = ft.KeyboardEvent("l", False, False, False, False)
#         typing_test.key_pressed(event)

#         assert typing_test.printed_text == "hel"
#         assert typing_test.letter_colors[2] == LetterColor.CORRECT

#         page.window_destroy()

#     ft.app(target=test)


# def test_key_pressed_wrong_key():
#     def test(page: ft.Page):
#         typing_test = get_typing_test(page)

#         # Test begin
#         typing_test.correct_text = "hello"
#         typing_test.printed_text = "he"

#         event = ft.KeyboardEvent("a", False, False, False, False)
#         typing_test.key_pressed(event)

#         assert typing_test.printed_text == "hea"
#         assert typing_test.letter_colors[2] == LetterColor.WRONG

#         page.window_destroy()

#     ft.app(target=test)


# def test_backspace_pressed():
#     def test(page: ft.Page):
#         typing_test = get_typing_test(page)

#         # Test begin
#         typing_test.correct_text = "hello"
#         typing_test.printed_text = "hea"

#         event = ft.KeyboardEvent("backspace", False, False, False, False)
#         typing_test.key_pressed(event)

#         assert typing_test.printed_text == "he"
#         assert typing_test.letter_colors[2] == LetterColor.UNUSED

#         page.window_destroy()

#     ft.app(target=test)
