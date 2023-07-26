import functools
import os
import sqlite3
from typing import Dict, List, Optional, Set, Union

ROUNDS = 4
INF = 2147483647
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def clean_year(year: Union[str, int]) -> str:
    """
    Clean the year string by standardising all input to YYYY, e.g. 2223.

    Args:
        year (Union[str, int]): The year string or integer.

    Returns:
        str: The cleaned year string.
    """
    year = str(year).strip().replace("/", "").replace(" ", "").replace("-", "")
    # Turns 20222023 to 2223
    if len(year) == 8:
        year = year[2] + year[3] + year[6] + year[7]
    return year


def clean_semester(semester: Union[str, int]) -> str:
    """
    Clean the semester string by removing leading/trailing spaces.

    Args:
        semester (Union[str, int]): The semester string or integer.

    Returns:
        str: The cleaned semester string.
    """
    return str(semester).strip()


def clean_ug_gd(ug_gd: str) -> str:
    """
    Clean the undergraduate/graduate string by converting to lowercase and
    removing leading/trailing spaces.

    Args:
        ug_gd (str): The undergraduate/graduate string.

    Returns:
        str: The cleaned undergraduate/graduate string.
    """
    return ug_gd.strip().lower()


def clean_code(code: str) -> str:
    """
    Clean the course code string by converting to uppercase and
    removing leading/trailing spaces.

    Args:
        code (str): The course code string.

    Returns:
        str: The cleaned course code string.
    """
    return code.strip().upper()


ClassDict = Dict[str, List[Dict[str, int]]]
CourseData = Dict[str, Union[str, ClassDict]]


def get_data(year: Union[str, int],
             semester: Union[str, int],
             ug_gd: str,
             code: str,
             conn: Optional[sqlite3.Connection] = None
             ) -> CourseData:
    """
    Retrieve data for a specific course from the database.
    The data is in the format of the following:
        'faculty': str,
        'department': str,
        'code': str,
        'title': str,
        'classes': class_dict

    The class dict has keys of the class name, for example "SG01" (Sectional
    teaching group 1). Its value is a list of length 4.

    Each element corresponds to the information in round 0, 1, 2 and 3.
    They have the following format:
        'demand': int,
        'vacancy': int,
        'successful_main': int,
        'successful_reserve': int,
        'quota_exceeded': int,
        'timetable_clashes': int,
        'workload_exceeded': int,
        'others': int,

    Args:
        year (Union[str, int]): The academic year.
        semester (Union[str, int]): The semester.
        ug_gd (str): The undergraduate/graduate indicator.
        code (str): The course code.
        conn (Optional[sqlite3.Connection]):
            Optional database connection object.

    Returns:
        CourseData: The course data.
    """
    # Clean arguments
    year = clean_year(year)
    semester = clean_semester(semester)
    ug_gd = clean_ug_gd(ug_gd)
    code = clean_code(code)

    # Establish the database connection if not provided
    if conn is None:
        conn = sqlite3.connect(os.path.join(BASE_DIR, 'database.db'))
    conn.row_factory = sqlite3.Row

    # Prepare the structure of returned value
    class_dict: ClassDict = {}
    output: Dict[str, Union[str, ClassDict]] = {
            'faculty': "",
            'department': "",
            'code': code,
            'title': "",
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

        # Get every matching class of the course code
        cursor = conn.execute(f"SELECT * FROM {TABLE_NAME} WHERE Code=?",
                              (code,))

        ROWS = cursor.fetchall()

        for row in ROWS:
            # Fill in the class dict
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

            # Logic to pad skipped rounds with blanks to ensure that
            # the list stays at length 4, corresponding to each round.
            if CLASSNAME in class_dict:
                class_dict[CLASSNAME].extend(
                        [BLANK for _
                         in range(round_number - len(class_dict[CLASSNAME]))])
                class_dict[CLASSNAME].append(result)
            else:
                class_dict[CLASSNAME] = [BLANK] * round_number
                class_dict[CLASSNAME].append(result)

    # Final padding of classes that don't have all the round information
    for key in class_dict:
        class_dict[key] += [BLANK] * (ROUNDS - len(class_dict[key]))

    # If nothing was found, throw an error.
    if not class_dict:
        raise ValueError(f"Course {code} not found.")

    # close the database connection if it was created here
    if conn is not None and conn.close is None:
        conn.close()

    return output


def get_set_of_all_codes(year: Union[str, int],
                         semester: Union[str, int],
                         ug_gd: str,
                         conn: Optional[sqlite3.Connection] = None
                         ) -> Set[str]:
    """
    Get a set of all known course codes in the history
    for a specific year, semester, and undergraduate/graduate.

    Args:
        year (Union[str, int]): The academic year.
        semester (Union[str, int]): The semester.
        ug_gd (str): The undergraduate/graduate indicator.
        conn (Optional[sqlite3.Connection]):
            Optional database connection object.

    Returns:
        Set[str]: A set of course codes.
    """
    # Clean arguments
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

        # get every code from the table, and add it to the set
        cursor = conn.execute(f"SELECT Code FROM {TABLE_NAME}")

        ROWS = cursor.fetchall()
        for row in ROWS:
            codes.add(row['Code'])

    # close the database connection if it was created here
    if conn is not None and conn.close is None:
        conn.close()

    # If nothing was found, throw an error.
    if not codes:
        raise ValueError("Data not found.")

    return codes


@functools.lru_cache
def get_all_data(year: Union[str, int],
                 semester: Union[str, int],
                 ug_gd: str) -> List[CourseData]:
    """
    Get data for all courses in a specific year, semester,
    and undergraduate/graduate.
    It will be in the form of a list of course data.
    Each element will be in the form of the output from get_data().

    Args:
        year (Union[str, int]): The academic year.
        semester (Union[str, int]): The semester.
        ug_gd (str): The undergraduate/graduate indicator.

    Returns:
        List[CourseData]: A list of course data.
    """
    conn = sqlite3.connect(os.path.join(BASE_DIR, 'database.db'))

    codes: Set[str] = get_set_of_all_codes(year, semester, ug_gd, conn)
    sorted_codes: List[str] = sorted(codes)

    output = []
    for code in sorted_codes:
        output.append(get_data(year, semester, ug_gd, code, conn))

    conn.close()

    return output
