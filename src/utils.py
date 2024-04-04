import os
import wget
import numpy as np
import pandas as pd
from src.constants import STATISTICS_FIELD_NAMES
from src import constants


def load_assets():
    font_path = "./assets/" + constants.FILE_NAMES["custom_font"]
    if not os.path.exists(font_path):
        os.makedirs("./assets")

        wget.download(constants.DOWNLOAD_URLS["custom_font"], out=font_path)

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
