import os
import sqlite3

ROUNDS = 4
INF = 2147483647
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_data(year, semester, ug_gd, code):
    code = code.upper()

    # establish the database connection
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'database.db'))
    conn.row_factory = sqlite3.Row

    class_dict = {}
    output = {'code': code, 'classes': class_dict, 'error': None}
    BLANK = {'demand': -1, 'vacancy': -1}

    # for each round, execute the SQL query
    for i in range(ROUNDS):
        TABLE_NAME = f"data_cleaned_{year}_{semester}_{ug_gd}_round_{i}"

        # check if table exists first
        cursor = conn.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (TABLE_NAME,))
        if cursor.fetchone() is None:
            output["error"] = f"History for the given year {year} semester {semester} ({ug_gd}) not found."
            return output

        cursor = conn.execute(f"SELECT * FROM {TABLE_NAME} WHERE Code=?",
                              (code,))

        ROWS = cursor.fetchall()

        for row in ROWS:
            CLASSNAME = row['Class']
            DEMAND = row['Demand']
            VACANCY = row['Vacancy']

            result = {'demand': DEMAND, 'vacancy': VACANCY}

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
