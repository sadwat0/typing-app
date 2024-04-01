import os
import matplotlib
import seaborn as sns
import numpy as np
import pandas as pd
import flet as ft
from src.constants import STATISTICS_FIELD_NAMES
from src.typing_test import TypingTest
from src.statistics_page import StatisticsPage
from src.heatmaps_page import HeatmapsPage

matplotlib.use("agg")
sns.set_theme()

color_scheme = {
    "background": "#242933",
    "nav_background": "#1c232e",
    "primary": "#ed4c57",  # red
    "secondary": "#f5efe9",  # white
    "tertiary": "#5a6173",  # gray
}

# Checking for saves file existence
if not os.path.exists("./saves"):
    os.makedirs("./saves")

if not os.path.isfile("./saves/data.csv"):
    with open("./saves/data.csv", "w", encoding="utf-8") as f:
        f.write(",".join(STATISTICS_FIELD_NAMES) + "\n")

if not os.path.isfile("./saves/heatmap.csv"):
    with open("./saves/heatmap.csv", "w", encoding="utf-8") as f:
        column_size = max(26, 33) ** 2
        df = pd.DataFrame(
            {
                "en": np.zeros(column_size, dtype=int),
                "ru": np.zeros(column_size, dtype=int),
            }
        )
        df.to_csv("./saves/heatmap.csv", index=False)


def main(page: ft.Page):
    """Main function, start application"""

    page.title = "Typing app"
    page.window_width = 1200
    page.window_height = 700
    page.bgcolor = color_scheme["background"]

    page.fonts = {"RobotoMono": "./assets/RobotoMono-VariableFont_wght.ttf"}

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


ft.app(target=main)
