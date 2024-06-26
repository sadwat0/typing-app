"""Realizes statistics page graphical class"""

import datetime
import pandas as pd
import flet as ft
from src.statistics_classes import Statistics
from src.constants import color_scheme
from src import constants


class StatisticsPage(ft.UserControl):
    """Graphical element for stats page"""

    class TestStatisticsVisualizer(ft.UserControl):
        """Graphical element for one test statistics"""

        def create_text_element(self, label: str, value: str) -> ft.Text:
            """Creates formated text graphical element"""

            return ft.Row(
                [
                    ft.Text(
                        f"{label}: ",
                        color=color_scheme["secondary"],
                        theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                    ),
                    ft.Text(
                        value,
                        color=color_scheme["primary"],
                        theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                    ),
                ],
                width=constants.STATISTICS_PAGE["test_content_width"],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )

        def __init__(self, index: int, statistics: Statistics):
            super().__init__()

            self.statistics = statistics

            self.index = index
            self.text_stats = ft.Column(
                [
                    self.create_text_element("WPM", f"{self.statistics.get_wpm():.1f}"),
                    self.create_text_element(
                        "ACCURACY", f"{self.statistics.get_accuracy():.1f}%"
                    ),
                    self.create_text_element("LANGUAGE", f"{self.statistics.language}"),
                    self.create_text_element(
                        "MODE",
                        (
                            f"{self.statistics.test_size} words"
                            if self.statistics.test_size_mode == "words"
                            else f"{self.statistics.test_size}s"
                        ),
                    ),
                    self.create_text_element(
                        "PUNCTUATION", "ON" if self.statistics.punctuation else "OFF"
                    ),
                    self.create_text_element(
                        "NUMBERS", "ON" if self.statistics.punctuation else "OFF"
                    ),
                    self.create_text_element(
                        "KEY PRESSES",
                        str(self.statistics.correct_key_presses)
                        + "/"
                        + str(self.statistics.total_key_presses),
                    ),
                    self.create_text_element(
                        "START",
                        f"{self.statistics.start_time.strftime(constants.DATE_FORMATS['stats_start_end_time'])}",
                    ),
                    self.create_text_element(
                        "END",
                        f"{self.statistics.end_time.strftime(constants.DATE_FORMATS['stats_start_end_time'])}",
                    ),
                ],
                spacing=constants.STATISTICS_PAGE["text_stats_spacing"],
            )

        def build(self):
            return ft.Container(
                ft.Column(
                    [
                        ft.Text(
                            f"TEST #{self.index + 1}",
                            color=color_scheme["secondary"],
                            theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                        ),
                        ft.Row([self.text_stats]),
                    ]
                ),
                padding=constants.STATISTICS_PAGE["test_padding"],
                border_radius=constants.STATISTICS_PAGE["test_border_radius"],
                width=constants.STATISTICS_PAGE["test_width"],
                bgcolor=color_scheme["nav_background"],
            )

    def __init__(self):
        super().__init__()

        self.list_content = []

        self.stats = pd.read_csv("./saves/" + constants.FILE_NAMES["data"])
        if len(self.stats) == 0:
            self.list_content = [
                ft.Text(
                    "You haven't passed any tests yet",
                    color=color_scheme["secondary"],
                    theme_style=ft.TextThemeStyle.HEADLINE_LARGE,
                )
            ]
        else:
            for index, row in self.stats.iloc[::-1].iterrows():
                statistics_object = Statistics(
                    test_size_mode=row["test_size_mode"],
                    test_size=row["test_size"],
                    language=row["language"],
                    punctuation=row["punctuation"],
                    numbers=row["numbers"],
                    start_time=datetime.datetime.strptime(
                        row["start_time"], constants.DATE_FORMATS["test_start_end_time"]
                    ),
                    end_time=datetime.datetime.strptime(
                        row["end_time"], constants.DATE_FORMATS["test_start_end_time"]
                    ),
                    total_key_presses=row["total_key_presses"],
                    correct_key_presses=row["correct_key_presses"],
                )

                self.list_content.append(
                    self.TestStatisticsVisualizer(index, statistics_object)
                )

    def build(self):
        return ft.ListView(
            self.list_content,
            expand=1,
            spacing=constants.STATISTICS_PAGE["spacing"],
            auto_scroll=False,
        )
