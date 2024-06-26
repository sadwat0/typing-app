"""Statistics and HeatmapStatistics classes"""

import datetime
from csv import DictWriter
import pandas as pd
import numpy as np
from src.constants import LANGUAGE_LETTERS, STATISTICS_FIELD_NAMES
from src import constants


class Statistics:
    """
    Stores information about running or completed test
    and calculates typing speed (cpm, wpm), accuracy
    """

    def __init__(
        self,
        test_size_mode: str | None = None,
        test_size: str | None = None,
        language: str | None = None,
        punctuation: bool = False,
        numbers: bool = False,
        start_time: datetime.datetime | None = None,
        end_time: datetime.datetime | None = None,
        total_key_presses: int = 0,
        correct_key_presses: int = 0,
    ):
        self.test_size_mode = test_size_mode
        self.test_size = test_size
        self.language = language

        self.start_time = start_time
        if start_time is None:
            self.start_time = datetime.datetime.now()

        # if None it means, that test is not over yer
        self.end_time = end_time

        self.total_key_presses = total_key_presses
        self.correct_key_presses = correct_key_presses

        self.punctuation = punctuation
        self.numbers = numbers

    def key_pressed(self, key: str, is_correct: bool | None = None):
        """Handles key press

        Args:
            key (str): allowed char or backspace
            is_correct (bool | None, optional): Must be not None if key != backspace.
        """

        if key != "backspace":
            self.total_key_presses += 1
            self.correct_key_presses += is_correct

    def get_accuracy(self) -> float:
        """Returns accuracy (in percents)"""

        if self.total_key_presses == 0:
            return constants.MAX_ACCURACY
        return (
            self.correct_key_presses / self.total_key_presses * constants.MAX_ACCURACY
        )

    def get_cpm(self) -> float:
        """Returns average cpm"""
        current_time = self.end_time
        if current_time is None:
            current_time = datetime.datetime.now()

        start_timestamp = self.start_time.timestamp()
        current_timestamp = current_time.timestamp()

        delta_minutes = (
            current_timestamp - start_timestamp
        ) / constants.SECONDS_IN_MINUTE

        if delta_minutes == 0:
            return constants.DEFAULT_CPM_WITH_NO_TIME

        return self.correct_key_presses / delta_minutes

    def get_wpm(self) -> float:
        """Returns average wpm (1 word == {constants.CHARACTERS_IN_WORD} chars)"""
        return self.get_cpm() / constants.CHARACTERS_IN_WORD

    def end(self):
        """Writes end_time with current time"""
        self.end_time = datetime.datetime.now()

    def save(self):
        """Saves to file"""
        stats_dict = {
            "wpm": self.get_wpm(),
            "accuracy": self.get_accuracy(),
            "test_size_mode": self.test_size_mode,
            "test_size": self.test_size,
            "language": self.language,
            "punctuation": self.punctuation,
            "numbers": self.numbers,
            "total_key_presses": self.total_key_presses,
            "correct_key_presses": self.correct_key_presses,
            "start_time": self.start_time.strftime(
                constants.DATE_FORMATS["test_start_end_time"]
            ),
            "end_time": self.end_time.strftime(
                constants.DATE_FORMATS["test_start_end_time"]
            ),
        }

        with open(
            "./saves/" + constants.FILE_NAMES["data"], "a", newline="", encoding="utf-8"
        ) as stats_file:
            DictWriter(stats_file, fieldnames=STATISTICS_FIELD_NAMES).writerow(
                stats_dict
            )


class HeatmapStatistics:
    """Calculates and stores error heatmap"""

    def __init__(self):
        df = pd.read_csv("./saves/" + constants.FILE_NAMES["heatmap"])

        en_length = len(constants.LANGUAGE_LETTERS["en"])
        ru_length = len(constants.LANGUAGE_LETTERS["ru"])

        self.stats = {
            "en": np.array(df["en"][: en_length**2]).reshape(en_length, en_length),
            "ru": np.array(df["ru"]).reshape(ru_length, ru_length),
        }

    def add_key_press(self, need_type: str, typed: str):
        """Updates stats"""

        # Not error press
        if need_type == typed:
            return

        if need_type in LANGUAGE_LETTERS["en"] and typed in LANGUAGE_LETTERS["en"]:
            need_index = LANGUAGE_LETTERS["en"].find(need_type)
            typed_index = LANGUAGE_LETTERS["en"].find(typed)

            self.stats["en"][need_index][typed_index] += 1
        elif need_type in LANGUAGE_LETTERS["ru"] and typed in LANGUAGE_LETTERS["ru"]:
            need_index = LANGUAGE_LETTERS["ru"].find(need_type)
            typed_index = LANGUAGE_LETTERS["ru"].find(typed)

            self.stats["ru"][need_index][typed_index] += 1

    def save(self):
        """Saves data to csv file"""

        df = pd.DataFrame(
            {
                "en": np.concatenate(
                    [
                        self.stats["en"].reshape(-1),
                        # adding zeros so length of cols will be same
                        np.zeros(
                            len(constants.LANGUAGE_LETTERS["ru"]) ** 2
                            - len(constants.LANGUAGE_LETTERS["en"]) ** 2,
                            dtype=int,
                        ),
                    ]
                ),
                "ru": self.stats["ru"].reshape(-1),
            }
        )

        df.to_csv("./saves/" + constants.FILE_NAMES["heatmap"], index=False)
