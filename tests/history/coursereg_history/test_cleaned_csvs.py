import csv
import os
import re
import unittest
from typing import Callable, Iterator, List


def is_int(val: str) -> bool:
    try:
        int(val)
        return True
    except ValueError:
        return False


def has_good_header(reader: Iterator[List[str]], file_path: str) -> None:
    header_row = next(reader)

    expected_header = ["Faculty", "Department", "Code",
                       "Title", "Class",
                       "Vacancy", "Demand",
                       "Successful_Main", "Successful_Reserve",
                       "Quota_Exceeded", "Timetable_Clashes",
                       "Workload_Exceeded", "Others"]

    if header_row != expected_header:
        raise ValueError(f"In {file_path}:"
                         f"{header_row} has incorrect column labels.")


def has_good_length(reader: Iterator[List[str]], file_path: str) -> None:
    for row in reader:
        if len(row) != 13:
            raise ValueError(f"In {file_path}:"
                             f"{row} has too few/many entries.")


def has_entries(reader: Iterator[List[str]], file_path: str) -> None:
    for row in reader:
        if any(item == "" for item in row):
            raise ValueError(f"In {file_path}:"
                             f"{row} has empty entries.")


def has_valid_course_codes(reader: Iterator[List[str]],
                           file_path: str) -> None:
    # Valid codes: LL5009GRSI, GESS1025
    course_code_pattern = r"^[A-Z]{2,4}\d{4}[A-Z]{0,4}$"

    # Skip the header row
    next(reader)

    for row in reader:
        course_code = row[2]
        if not re.match(course_code_pattern, course_code):
            raise ValueError(f"In {file_path}:"
                             f"{course_code} did not match the regex.")


def has_number_data(reader: Iterator[List[str]], file_path: str) -> None:
    # Skip the header row
    next(reader)

    for row in reader:
        if not all(is_int(val) for val in row[5:]):
            raise ValueError(f"In {file_path}:"
                             f"{row[5:]} did not have number data.")


def check_all_csvs(check_func: Callable[[Iterator[List[str]], str],
                                        None]) -> bool:
    current_file_directory = os.path.dirname(os.path.abspath(__file__))
    csv_directory = os.path.abspath(
        os.path.join(current_file_directory, "..", "..",
                     "src", "history", "coursereg_history", "data", "cleaned"))

    for root, _, files in os.walk(csv_directory):
        for file in files:
            if not file.endswith(".csv"):
                pass

            file_path = os.path.join(root, file)
            with open(file_path, "r") as f:
                reader = csv.reader(f)
                check_func(reader, file_path)

    return True


class MainTestCase(unittest.TestCase):
    def test_header(self) -> None:
        self.assertTrue(check_all_csvs(has_good_header))

    def test_length(self) -> None:
        self.assertTrue(check_all_csvs(has_good_length))

    def test_non_blank_entries(self) -> None:
        self.assertTrue(check_all_csvs(has_entries))

    def test_number_entries(self) -> None:
        self.assertTrue(check_all_csvs(has_number_data))

    def test_course_codes(self) -> None:
        self.assertTrue(check_all_csvs(has_valid_course_codes))


if __name__ == "__main__":
    unittest.main()
