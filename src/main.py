import argparse
from colorama import Fore, Style
import math
import sqlite3

ROUNDS = 4
INF = 2147483647
BLANK = f"{Fore.LIGHTBLACK_EX}N/A{Style.RESET_ALL}"


def colour_course(x):
    return f"{Fore.YELLOW}{x}{Style.RESET_ALL}"


def colour_percent(x):
    x = float(x)
    if math.isnan(x):
        return f"{Fore.RED}NaN{Style.RESET_ALL}"
    if x == 100:
        return f"{Fore.RESET}{x}{Style.RESET_ALL}"
    elif x < 100:
        return f"{Fore.GREEN}{x}{Style.RESET_ALL}"
    else:
        return f"{Fore.RED}{x}{Style.RESET_ALL}"


def colour(demand, vacancy):
    if demand == vacancy:
        return f"{Fore.RESET}{demand} / {vacancy}{Style.RESET_ALL}"
    elif demand > vacancy:
        return f"{Fore.RED}{demand} / {vacancy}{Style.RESET_ALL}"
    else:
        return f"{Fore.GREEN}{demand} / {vacancy}{Style.RESET_ALL}"


def query_db(year, semester, ug_gd, code, percentage):
    # establish the database connection
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row

    class_dict = {}

    # for each round, execute the SQL query
    for i in range(ROUNDS):
        TABLE_NAME = f"data_cleaned_{year}_{semester}_{ug_gd}_round_{i}"
        cursor = conn.execute(f"SELECT * FROM {TABLE_NAME} WHERE Code=?",
                              (code,))

        ROWS = cursor.fetchall()
        if ROWS:
            for row in ROWS:
                CLASSNAME = row['Class']
                DEMAND = row['Demand']
                vacancy = row['Vacancy']
                PERCENTAGE = round(
                    DEMAND / vacancy * 100
                ) if vacancy > 0 else 'NaN'

                if vacancy == INF:
                    vacancy = '∞'

                result = colour_percent(
                    PERCENTAGE
                ) if percentage else colour(DEMAND, vacancy)

                if CLASSNAME in class_dict:
                    class_dict[CLASSNAME].extend(
                            [BLANK for _
                             in range(i - len(class_dict[CLASSNAME]))])
                    class_dict[CLASSNAME].append(result)
                else:
                    class_dict[CLASSNAME] = [BLANK] * i
                    class_dict[CLASSNAME].append(result)

    # Pad classes that don't have all the round information
    for key in class_dict:
        class_dict[key] += [BLANK] * (ROUNDS - len(class_dict[key]))

    if (len(class_dict) > 0):
        MAX_KEY_LEN = max(len(key) for key in class_dict.keys())
        MAX_VALUE_LEN = max(len(str(val)) for sublist in class_dict.values()
                            for val in sublist)
        # Print in the desired format
        print(colour_course(code))
        for key, value in class_dict.items():
            PADDED_VALUES = [f"{v:{MAX_VALUE_LEN}}" for v in value]
            print(f"{key:{MAX_KEY_LEN}}: {' -> '.join(PADDED_VALUES)}")
    else:
        print(colour_course(f"{code} NOT FOUND"))

    # close the database connection
    conn.close()


# Function to convert the argument to int, or leave it as str if not possible
def int_or_str(value):
    try:
        return int(value)
    except ValueError:
        return value


# setup command line argument parsing
parser = argparse.ArgumentParser(description='Query course data.')
parser.add_argument('-y', '--year',
                    type=int_or_str,
                    help='read reports from this year')
parser.add_argument('-s', '--semester',
                    type=int_or_str,
                    help='read reports from this semester')
parser.add_argument('-t', '--type',
                    type=str,
                    help='read reports from "ug" or "gd"',
                    default='ug')
parser.add_argument('-c', '--course_codes',
                    type=str, nargs='+',
                    help='list of course codes')
parser.add_argument('-p', '--percentage',
                    action='store_true',
                    help='change the format to a percentage')
parser.add_argument('-f', '--file',
                    type=str,
                    help='read input from a file containing course codes')

args = parser.parse_args()

course_codes = args.course_codes or []

if (args.file):
    with open(args.file, 'r') as file:
        course_codes = course_codes + [line.strip() for line in file]

# query the database
for course_code in course_codes:
    query_db(args.year, args.semester, args.type, course_code, args.percentage)
