import argparse
from colorama import Fore, Style
import math
import os
from typing import Dict, Union

ROUNDS = 4
INF = 2147483647
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

from api import get_data


def colour_na(colour: bool) -> str:
    if colour:
        return f"{Fore.LIGHTBLACK_EX}N/A{Style.RESET_ALL}"
    else:
        return "N/A"


def colour_course(x: str, colour: bool) -> str:
    if colour:
        return f"{Fore.YELLOW}{x}{Style.RESET_ALL}"
    else:
        return x


def colour_percent(x: float, colour: bool) -> str:
    x = float(x)
    if math.isnan(x):
        if colour:
            return f"{Fore.RED}NaN{Style.RESET_ALL}"
        else:
            return "NaN"
    elif not colour:
        return str(x)
    elif x == 100:
        return f"{Fore.RESET}{x}{Style.RESET_ALL}"
    elif x < 100:
        return f"{Fore.GREEN}{x}{Style.RESET_ALL}"
    else:
        return f"{Fore.RED}{x}{Style.RESET_ALL}"


def format(info: Dict[str, int], colour: bool, percentage: bool) -> str:
    DEMAND = info["demand"]
    vacancy = info["vacancy"]
    if DEMAND == -1 and vacancy == -1:
        return colour_na(colour)
    elif percentage:
        PERCENTAGE = round(
            DEMAND / vacancy * 100
        ) if vacancy > 0 else float('nan')

        return colour_percent(PERCENTAGE, colour)
    else:
        return colour_demand_vacancy(DEMAND, vacancy, colour)


def colour_demand_vacancy(demand: int, vacancy: int, colour: bool) -> str:
    if vacancy is INF:
        if not colour:
            return f"{demand} / ∞"
        else:
            return f"{Fore.GREEN}{demand} / ∞{Style.RESET_ALL}"

    if not colour:
        return f"{demand} / {vacancy}"
    elif demand == vacancy:
        return f"{Fore.RESET}{demand} / {vacancy}{Style.RESET_ALL}"
    elif demand > vacancy:
        return f"{Fore.RED}{demand} / {vacancy}{Style.RESET_ALL}"
    else:
        return f"{Fore.GREEN}{demand} / {vacancy}{Style.RESET_ALL}"


def print_data(year: Union[str, int],
               semester: Union[str, int],
               ug_gd: str,
               code: str,
               percentage: bool,
               colour: bool,
               verbose: bool):
    if verbose:
        print(get_data(year, semester, ug_gd, code))
        return

    DATA = get_data(year, semester, ug_gd, code)

    CLASSES = DATA['classes']

    if (len(CLASSES) > 0):
        print(colour_course(DATA['code'], colour))
    else:
        print(colour_course(f"{code} NOT FOUND", colour))

    MAX_KEY_LEN = max(len(key) for key in CLASSES.keys())
    MAX_VALUE_LEN = max(len(str(format(val, colour, percentage)))
                        for sublist in CLASSES.values() for val in sublist)

    for CLASS in CLASSES:
        class_dict = {CLASS: [format(info, colour, percentage)
                              for info in CLASSES[CLASS]]}

        if (len(class_dict) > 0):
            # Print in the desired format
            for key, value in class_dict.items():
                PADDED_VALUES = [f"{v:{MAX_VALUE_LEN}}" for v in value]
                print(f"{key:{MAX_KEY_LEN}}: {' -> '.join(PADDED_VALUES)}")


# Function to convert the argument to int, or leave it as str if not possible
def int_or_str(value: Union[str, int]) -> Union[str, int]:
    try:
        return int(value)
    except ValueError:
        return value


def main() -> None:
    parser = argparse.ArgumentParser(description='Query course data.')
    parser.add_argument('-y', '--year',
                        type=int_or_str,
                        help=(
                            'read reports from this academic year. '
                            'This argument is required.\n'
                            'format: (2223 or "22/23" or "22-23" or "2022").\n'
                            'Note: The academic year is based on '
                            'the starting year.'),
                        required=True)
    parser.add_argument('-s', '--semester',
                        type=int_or_str,
                        help=(
                            'read reports from this semester. '
                            'This argument is required.\n'
                            'format: (1 or 2)'),
                        required=True)
    parser.add_argument('-t', '--type',
                        type=str,
                        help=(
                            'read reports from "ug" (undergraduate) '
                            'or "gd" (graduate).\n'
                            'format: ("ug" or "gd" or "undergraduate" '
                            'or "graduate")'),
                        default='ug')
    parser.add_argument('-c', '--course_codes',
                        type=str, nargs='+',
                        help='list of course codes')
    parser.add_argument('-p', '--percentage',
                        action='store_true',
                        help='converts some unspecified value to a percentage')
    parser.add_argument('-f', '--file',
                        type=str,
                        help='read input from a file containing course codes')
    parser.add_argument('--no-colour',
                        action='store_true',
                        help='ensures the output has no colour')
    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='returns the full API call')

    args = parser.parse_args()

    # check if neither -c nor -f is provided
    if args.course_codes is None and args.file is None:
        parser.error("at least one of -c/--course_codes or -f/--file required")

    course_codes = args.course_codes or []

    if (args.file):
        with open(args.file, 'r') as file:
            course_codes = course_codes + [line.strip() for line in file]

    # query the database
    for course_code in course_codes:
        try:
            print_data(args.year, args.semester, args.type, course_code,
                       args.percentage, not args.no_colour, args.verbose)
        except ValueError as e:
            print(e)


if __name__ == "__main__":
    main()
