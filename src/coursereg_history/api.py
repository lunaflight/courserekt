import os
import sqlite3
from typing import Dict, List, Optional, Set, Union

ROUNDS = 4
INF = 2147483647
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ClassDict = Dict[str, List[Dict[str, int]]]


def clean_year(year):
    year = str(year).strip().replace("/", "").replace(" ", "").replace("-", "")
    # Turns 20222023 to 2223
    if len(year) == 8:
        year = year[2] + year[3] + year[6] + year[7]
    return year


def clean_semester(semester):
    return str(semester).strip()


def clean_ug_gd(ug_gd):
    return ug_gd.strip().lower()


def clean_code(code):
    return code.strip().upper()


def get_data(year: Union[str, int],
             semester: Union[str, int],
             ug_gd: str,
             code: str,
             conn: Optional[sqlite3.Connection] = None) -> Dict[str, Optional[Union[str, ClassDict]]]:
    year = clean_year(year)
    semester = clean_semester(semester)
    ug_gd = clean_ug_gd(ug_gd)
    code = clean_code(code)

    # Establish the database connection if not provided
    if conn is None:
        conn = sqlite3.connect(os.path.join(BASE_DIR, 'database.db'))
    conn.row_factory = sqlite3.Row

    class_dict: ClassDict = {}
    output = {
            'faculty': None,
            'department': None,
            'code': code,
            'title': None,
            'classes': class_dict}
    BLANK = {'demand': -1,
             'vacancy': -1,
             'successful_main': -1,
             'successful_reserve': -1,
             'quota_exceeded': -1,
             'timetable_clashes': -1,
             'workload_exceeded': -1,
             'others': -1}

    # for each round, execute the SQL query
    for round_number in range(ROUNDS):
        TABLE_NAME = (
                f"data_cleaned_{year}_{semester}_{ug_gd}_round_{round_number}")

        # check if table exists first
        cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (TABLE_NAME,))
        if cursor.fetchone() is None:
            continue

        cursor = conn.execute(f"SELECT * FROM {TABLE_NAME} WHERE Code=?",
                              (code,))

        ROWS = cursor.fetchall()

        for row in ROWS:
            CLASSNAME = row['Class']
            output['faculty'] = row['Faculty']
            output['department'] = row['Department']
            output['code'] = row['Code']
            output['title'] = row['Title']

            result = {'demand': row['Demand'],
                      'vacancy': row['Vacancy'],
                      'successful_main': row['Successful (Main)'],
                      'successful_reserve': row['Successful (Reserve)'],
                      'quota_exceeded': row['Quota Exceeded'],
                      'timetable_clashes': row['Timetable Clashes'],
                      'workload_exceeded': row['Workload Exceeded'],
                      'others': row['Others']}

            if CLASSNAME in class_dict:
                class_dict[CLASSNAME].extend(
                        [BLANK for _
                         in range(round_number - len(class_dict[CLASSNAME]))])
                class_dict[CLASSNAME].append(result)
            else:
                class_dict[CLASSNAME] = [BLANK] * round_number
                class_dict[CLASSNAME].append(result)

    # Pad classes that don't have all the round information
    for key in class_dict:
        class_dict[key] += [BLANK] * (ROUNDS - len(class_dict[key]))

    if len(class_dict) == 0:
        raise ValueError(f"Course {code} not found.")

    # close the database connection if it was created here
    if conn is not None and conn.close is None:
        conn.close()

    return output


def get_set_of_all_codes(year: Union[str, int],
                         semester: Union[str, int],
                         ug_gd: str,
                         conn: Optional[sqlite3.Connection] = None):
    year = clean_year(year)
    semester = clean_semester(semester)
    ug_gd = clean_ug_gd(ug_gd)

    codes: Set[str] = set()

    # Establish the database connection if not provided
    if conn is None:
        conn = sqlite3.connect(os.path.join(BASE_DIR, 'database.db'))
    conn.row_factory = sqlite3.Row

    # for each round, execute the SQL query
    for round_number in range(ROUNDS):
        TABLE_NAME = (
                f"data_cleaned_{year}_{semester}_{ug_gd}_round_{round_number}")

        # check if table exists first
        cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (TABLE_NAME,))
        if cursor.fetchone() is None:
            continue

        cursor = conn.execute(f"SELECT Code FROM {TABLE_NAME}")

        ROWS = cursor.fetchall()
        for row in ROWS:
            codes.add(row['Code'])

    # close the database connection if it was created here
    if conn is not None and conn.close is None:
        conn.close()

    if not codes:
        raise ValueError("Data not found.")

    return codes


def get_all_data(year: Union[str, int],
                 semester: Union[str, int],
                 ug_gd: str):
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'database.db'))

    codes = get_set_of_all_codes(year, semester, ug_gd, conn)
    codes = sorted(codes)

    output = []
    for code in codes:
        output.append(get_data(year, semester, ug_gd, code, conn))

    conn.close()

    return output
