"""Relizes heatmaps page graphical element"""

import matplotlib.pyplot as plt
import seaborn as sns
import flet as ft
from src.constants import LANGUAGE_LETTERS, color_scheme
from src.statistics_classes import HeatmapStatistics


class HeatmapsPage(ft.UserControl):
    """Heatmaps page graphical class"""

    class LanguageHeatmap(ft.UserControl):
        """One of heatmaps"""

        def __init__(self, language: str, heatmap_statistics: HeatmapStatistics):
            super().__init__()
            self.language = language
            self.heatmap = None

            plt.figure(figsize=(7, 7))
            ax = plt.axes()

            heatmap = sns.heatmap(
                heatmap_statistics.stats[language],
                annot=True,
                xticklabels=LANGUAGE_LETTERS[language],
                yticklabels=LANGUAGE_LETTERS[language],
                cmap="coolwarm",
                cbar=False,
                ax=ax,
                square=True,
            )

            ax.set_title(f"Language: {language}")
            plt.xlabel("Typed")
            plt.ylabel("Correct")

            fig = heatmap.get_figure()
            fig.savefig(
                f"./saves/heatmaps_{language}.png",
                transparent=True,
                bbox_inches="tight",
            )

            self.heatmap = ft.Image(
                src=f"./saves/heatmaps_{language}.png",
                width=500,
                height=500,
                fit=ft.ImageFit.CONTAIN,
            )

        def build(self):
            return ft.Container(
                self.heatmap,
                bgcolor=color_scheme["secondary"],
                width=500,
                height=500,
                border_radius=20,
                padding=ft.padding.only(top=10, bottom=10, right=20),
            )

    def __init__(self):
        super().__init__()

        self.stats = HeatmapStatistics()

        self.heatmaps = [
            self.LanguageHeatmap(language, self.stats) for language in ["en", "ru"]
        ]

    def build(self):
        return ft.Row(self.heatmaps, alignment=ft.MainAxisAlignment.SPACE_AROUND)
