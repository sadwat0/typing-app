import datetime
from unittest.mock import patch, MagicMock
from src.constants import LANGUAGE_LETTERS, STATISTICS_FIELD_NAMES
from src import constants
from src.statistics_classes import Statistics, HeatmapStatistics
import numpy as np
import pandas as pd


@patch("src.statistics_classes.datetime")
def test_statistics_init(mock_datetime):
    mock_datetime.datetime.now.return_value = datetime.datetime(2023, 1, 1)

    stats = Statistics(
        test_size_mode="time",
        test_size="1",
        language="en",
        punctuation=True,
        numbers=True,
    )

    assert stats.test_size_mode == "time"
    assert stats.test_size == "1"
    assert stats.language == "en"
    assert stats.start_time == datetime.datetime(2023, 1, 1)
    assert stats.end_time is None
    assert stats.total_key_presses == 0
    assert stats.correct_key_presses == 0
    assert stats.punctuation is True
    assert stats.numbers is True


def test_statistics_key_pressed():
    stats = Statistics()
    stats.key_pressed("a", is_correct=True)
    assert stats.total_key_presses == 1
    assert stats.correct_key_presses == 1
    stats.key_pressed("backspace")
    assert stats.total_key_presses == 1
    assert stats.correct_key_presses == 1


def test_statistics_get_accuracy():
    stats = Statistics()
    assert stats.get_accuracy() == 100.0
    stats.total_key_presses = 10
    stats.correct_key_presses = 8
    assert stats.get_accuracy() == 80.0


@patch("src.statistics_classes.datetime")
def test_statistics_get_cpm(mock_datetime):
    stats = Statistics()
    mock_datetime.datetime.now.return_value = datetime.datetime(2023, 1, 1, 0, 1)
    stats.start_time = datetime.datetime(2023, 1, 1)
    stats.correct_key_presses = 300
    assert stats.get_cpm() == 300.0


def test_statistics_get_wpm():
    stats = Statistics()
    stats.correct_key_presses = 300
    with patch.object(stats, "get_cpm", return_value=300):
        assert stats.get_wpm() == 60.0
