import os
import wget
import matplotlib
import seaborn as sns
import numpy as np
import pandas as pd
import flet as ft
from src.constants import STATISTICS_FIELD_NAMES, color_scheme
from src import constants
from src.typing_test import TypingTest
from src.statistics_page import StatisticsPage
from src.heatmaps_page import HeatmapsPage

matplotlib.use("agg")
sns.set_theme()


def main(page: ft.Page):
    """Main function, start application"""

    page.title = "Typing app"
    page.window_width = 1200
    page.window_height = 700
    page.bgcolor = color_scheme["background"]

    page.fonts = {"RobotoMono": "./assets/" + constants.FILE_NAMES["custom_font"]}

    typing_test = TypingTest(page)

    def route_change(_):
        page.views.clear()

        if page.route == "/":
            page.views.append(
                ft.View(
                    "/",
                    [
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    "Statistics", on_click=lambda _: page.go("/stats")
                                ),
                                ft.ElevatedButton(
                                    "Heatmaps", on_click=lambda _: page.go("/heatmaps")
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Divider(),
                        typing_test.visual_element,
                    ],
                    bgcolor=color_scheme["background"],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )

            typing_test.can_type = True
        elif page.route == "/stats":
            list_view_builder = StatisticsPage()

            page.views.append(
                ft.View(
                    "/stats",
                    [
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    "Main page", on_click=lambda _: page.go("/")
                                ),
                                ft.ElevatedButton(
                                    "Heatmaps", on_click=lambda _: page.go("/heatmaps")
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Divider(),
                        list_view_builder.build(),
                    ],
                    bgcolor=color_scheme["background"],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )

            typing_test.can_type = False
        elif page.route == "/heatmaps":
            page.views.append(
                ft.View(
                    "/heatmaps",
                    [
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    "Main page", on_click=lambda _: page.go("/")
                                ),
                                ft.ElevatedButton(
                                    "Statistics", on_click=lambda _: page.go("/stats")
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.Divider(),
                        HeatmapsPage(),
                    ],
                    bgcolor=color_scheme["background"],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )
            )

            typing_test.can_type = False

        page.update()

        if page.route == "/":
            typing_test.restart()

    page.on_route_change = route_change
    page.go(page.route)

    page.on_keyboard_event = typing_test.key_pressed
    page.update()


if __name__ == "__main__":
    # Checking for saves file existence

    FONT_PATH = "./assets/" + constants.FILE_NAMES["custom_font"]
    if not os.path.exists(FONT_PATH):
        os.makedirs("./assets")

        wget.download(constants.DOWNLOAD_URLS["custom_font"], out=FONT_PATH)

    for language in ["en", "ru"]:
        language_path = (
            "./assets/vocabulary/" + constants.FILE_NAMES[f"language_{language}"]
        )

        if not os.path.exists("./assets/vocabulary"):
            os.makedirs("./assets/vocabulary")

        if not os.path.exists(language_path):
            wget.download(
                constants.DOWNLOAD_URLS[f"language_{language}"], out=language_path
            )

    if not os.path.exists("./saves"):
        os.makedirs("./saves")

    if not os.path.isfile("./saves/" + constants.FILE_NAMES["data"]):
        with open(
            "./saves/" + constants.FILE_NAMES["data"], "w", encoding="utf-8"
        ) as f:
            f.write(",".join(STATISTICS_FIELD_NAMES) + "\n")

    if not os.path.isfile("./saves/" + constants.FILE_NAMES["heatmap"]):
        with open(
            "./saves/" + constants.FILE_NAMES["heatmap"], "w", encoding="utf-8"
        ) as f:
            max_language_length = 0
            for letters in constants.LANGUAGE_LETTERS.values():
                max_language_length = max(max_language_length, len(letters))

            column_size = max_language_length**2
            df = pd.DataFrame(
                {
                    "en": np.zeros(column_size, dtype=int),
                    "ru": np.zeros(column_size, dtype=int),
                }
            )
            df.to_csv("./saves/" + constants.FILE_NAMES["heatmap"], index=False)

    ft.app(target=main)
