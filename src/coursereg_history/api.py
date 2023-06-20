import os
import sqlite3
from typing import Dict, List, Optional, Union

ROUNDS = 4
INF = 2147483647
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ClassDict = Dict[str, List[Dict[str, int]]]


def get_data(year: Union[str, int],
             semester: Union[str, int],
             ug_gd: str,
             code: str) -> Dict[str, Optional[Union[str, ClassDict]]]:
    year = str(year).strip().replace("/", "").replace(" ", "").replace("-", "")
    # Turns 20222023 to 2223
    if len(year) == 8:
        year = year[2] + year[3] + year[6] + year[7]
    semester = str(semester).strip()
    ug_gd = ug_gd.strip().lower()
    code = code.strip().upper()

    # establish the database connection
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'database.db'))
    conn.row_factory = sqlite3.Row

    class_dict: ClassDict = {}
    output = {
            'faculty': None,
            'department': None,
            'code': code,
            'title': None,
            'classes': class_dict,
            'error': None}
    BLANK = {'demand': -1,
             'vacancy': -1,
             'successful_main': -1,
             'successful_reserve': -1,
             'quota_exceeded': -1,
             'timetable_clashes': -1,
             'workload_exceeded': -1,
             'others': -1}

    # for each round, execute the SQL query
    for i in range(ROUNDS):
        TABLE_NAME = f"data_cleaned_{year}_{semester}_{ug_gd}_round_{i}"

        # check if table exists first
        cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (TABLE_NAME,))
        if cursor.fetchone() is None:
            output["error"] = (
                f"History for the given year {year} semester {semester} "
                f"({ug_gd}) not found."
                )
            return output

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
                         in range(i - len(class_dict[CLASSNAME]))])
                class_dict[CLASSNAME].append(result)
            else:
                class_dict[CLASSNAME] = [BLANK] * i
                class_dict[CLASSNAME].append(result)

    # Pad classes that don't have all the round information
    for key in class_dict:
        class_dict[key] += [BLANK] * (ROUNDS - len(class_dict[key]))

    if len(class_dict) == 0:
        output["error"] = f"Course {code} not found."

    # close the database connection
    conn.close()
    return output
