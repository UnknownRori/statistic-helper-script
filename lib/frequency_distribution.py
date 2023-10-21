"""
This module is used to calculate frequency distribution
for my campus purposes, i'm quite lazy so i want to automated the process
TODO : clean up this shit
"""

from typing import TypeVar
from math import floor, log10
from utils import convert_list_to_list_float
from tabulate import tabulate
import json

T = TypeVar('T')
FrequencyDistributionRaw = dict[tuple[float, float], list[float]]
FrequencyDistributionStr = dict[str, list[float]]


class DataSet:
    """
    A class to represent dataset
    """
    _data: list[float]

    def __init__(self, data: list[float]) -> None:
        data.sort()
        self._data = data
        pass

    def first(self) -> float:
        return self._data[0]

    def last(self) -> float:
        return self._data[-1]

    def val_range(self) -> float:
        return self.last() - self.first()

    def class_interval(self) -> float:
        return class_interval(len(self._data))

    def length_class_interval(self, class_interval: int) -> float:
        return self.val_range() / class_interval

    def frequency_distribution(self, length_interval: int, max_start: int | None = None) -> FrequencyDistributionRaw:
        frequency: FrequencyDistributionRaw = {}

        def find_frequency(low: float, high: float, data: list[float]):
            if high < self.first():
                return

            for value in data:
                if low <= value <= high:
                    key = (low, high)
                    if key in frequency:
                        frequency[key].append(value)
                    else:
                        frequency[key] = [value]

            high = low - 1
            low = high - length_interval
            find_frequency(low, high, data)

        if max_start is None:
            high = self.last()
        else:
            high = max_start
        low = high - length_interval

        find_frequency(low, high, self._data)

        return frequency

    def __str__(self) -> str:
        return self._data.__str__()


def class_interval(n) -> float:
    return 1 + 3.3 * log10(n)


def convert_freqency_dict(frequency: FrequencyDistributionRaw) -> FrequencyDistributionStr:
    temp = {}
    for key, value in frequency.items():
        temp[f"{key[1]}-{key[0]}"] = value

    return temp


def print_tabulate(frequency: FrequencyDistributionStr, data_count: int):
    temp: list[list[str | float]] = []

    for key, value in frequency.items():
        data: list[str | float] = [
            key, len(value), (len(value) / data_count) * 100]
        temp.append(data)

    total_f_absolute = 0
    total_f_relative = 0
    for i in temp:
        total_f_absolute += i[1]
        total_f_relative += i[2]

    temp.append(["Total", total_f_absolute, total_f_relative])
    print(tabulate(temp, headers=[
          "Range", "f absolute", "f relative"], tablefmt="github"))


def get_input() -> list[str]:
    """
    Get the input from the user it will print out something
    Along the way
    """
    data = input("What data looks like (10 20.3 12) : ")
    data = data.split(" ")

    return data


if __name__ == "__main__":
    print("==============================")
    print("=== Frequency Distribution ===")
    print("==============================")
    print("")

    data = get_input()
    data = convert_list_to_list_float(data).unwrap()
    data_set = DataSet(data)
    total_data = len(data)
    print(f"Total  : `{total_data}`")
    print(f"Data   : `{data_set}`")

    data_range = data_set.val_range()
    print(f"Ranges : `{data_range}`")

    data_class_interval = data_set.class_interval()
    data_class_interval_floor = floor(data_class_interval)
    print(
        f"Class Interval: `{data_class_interval}` -> `{data_class_interval_floor}` | 1 + 3.3 * log10(`{total_data}`)")

    length_class_interval = data_set.length_class_interval(
        data_class_interval_floor)
    length_class_interval_floor = floor(length_class_interval)
    print(
        f"Length Class Interval: `{length_class_interval}` -> `{length_class_interval_floor}` | `{data_range}` / `{data_class_interval_floor}`")
    distribution = data_set.frequency_distribution(
        length_class_interval_floor, max_start=100)
    distribution_str = convert_freqency_dict(distribution)
    # print(json.dumps(distribution_str, indent=2))
    print_tabulate(distribution_str, len(data))

    pass
