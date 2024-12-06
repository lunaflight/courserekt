import functools
import re
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Union

# Round 0 was discontinued in AY 24/25
PRE_2425_YEARS = ("2122", "2223", "2324")
PRE_2425_ROUNDS = (0, 1, 2, 3)
POST_2425_ROUNDS = (1, 2, 3)

INF = 2147483647
NA = -1
BASE_DIR = Path(Path(__file__).resolve()).parent


def _clean_year(year: Union[str, int]) -> str:
    """
    Year strings are either "YYYY[ /-]YYYY" or "YYYY".

    Clean the year string by standardising all input to YYYY, e.g. 2223.

    Args:
    ----
        year (Union[str, int]): The year string or integer.

    Returns:
    -------
        str: The cleaned year string.
    """
    year = str(year).strip().replace("/", "").replace(" ", "").replace("-", "")

    # If the year string is YYYY[ /-]YYYY, standardise it.
    if re.match(r"[0-9]{8}", year):
        year = year[2:4] + year[6:]

    return year


def _clean_semester(semester: Union[str, int]) -> str:
    """
    Clean the string to 1 or 2.

    Clean the semester string by removing leading/trailing spaces.

    Args:
    ----
        semester (Union[str, int]): The semester string or integer.

    Returns:
    -------
        str: The cleaned semester string.
    """
    return str(semester).strip()


def _clean_ug_gd(ug_gd: str) -> str:
    """
    Clean the string to "UG" or "GD".

    Clean the undergraduate/graduate string by converting to lowercase and
    removing leading/trailing spaces.

    Args:
    ----
        ug_gd (str): The undergraduate/graduate string.

    Returns:
    -------
        str: The cleaned undergraduate/graduate string.
    """
    return ug_gd.strip().lower()


def _clean_code(code: str) -> str:
    """
    Clean the course code to XX1234X.

    Clean the course code string by converting to uppercase and
    removing leading/trailing spaces.

    Args:
    ----
        code (str): The course code string.

    Returns:
    -------
        str: The cleaned course code string.
    """
    return code.strip().upper()


ClassDict = dict[str, list[dict[str, int]]]
CourseData = dict[str, Union[str, ClassDict]]


def get_round_numbers(year: Union[str, int]) -> tuple[int, ...]:
    """
    Get a tuple of round numbers for a particular academic year.

    Args:
    ----
        year (Union[str, int]): The academic year.

    Returns:
    -------
        tuple[int]: A tuple of round numbers.
    """

    year = _clean_year(year)
    return PRE_2425_ROUNDS if year in PRE_2425_YEARS else POST_2425_ROUNDS


def get_data(year: Union[str, int],
             semester: Union[str, int],
             ug_gd: str,
             code: str,
             conn: Union[sqlite3.Connection, None] = None,
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
    ----
        year (Union[str, int]): The academic year.
        semester (Union[str, int]): The semester.
        ug_gd (str): The undergraduate/graduate indicator.
        code (str): The course code.
        conn (Optional[sqlite3.Connection]):
            Optional database connection object.

    Returns:
    -------
        CourseData: The course data.
    """
    # Clean arguments
    year = _clean_year(year)
    semester = _clean_semester(semester)
    ug_gd = _clean_ug_gd(ug_gd)
    code = _clean_code(code)

    # Establish the database connection if not provided
    if conn is None:
        conn = sqlite3.connect(Path(BASE_DIR) / "database.db")
    conn.row_factory = sqlite3.Row

    # Prepare the structure of returned value
    class_dict: ClassDict = {}
    output: dict[str, Union[str, ClassDict]] = {
        "faculty": "",
        "department": "",
        "code": code,
        "title": "",
        "classes": class_dict}
    BLANK = {"ug": -1,
             "gd": -1,
             "dk": -1,
             "ng": -1,
             "cpe": -1,
             "demand": -1,
             "vacancy": -1,
             "successful_main": -1,
             "successful_reserve": -1,
             "quota_exceeded": -1,
             "timetable_clashes": -1,
             "workload_exceeded": -1,
             "others": -1}

    # for each round, execute the SQL query
    round_numbers = get_round_numbers(year)
    for index, round_number in enumerate(round_numbers):
        TABLE_NAME = (
            "src_history_merged_"
            f"{year}_{semester}_{ug_gd}_round_{round_number}")

        if not pdf_exists(year, semester, ug_gd, round_number):
            continue

        # Get every matching class of the course code
        cursor = conn.execute(f"SELECT * FROM {TABLE_NAME} WHERE Code=?",
                              (code,))

        ROWS = cursor.fetchall()

        for row in ROWS:
            # Fill in the class dict
            CLASSNAME = row["Class"]
            output["faculty"] = row["Faculty"]
            output["department"] = row["Department"]
            output["code"] = row["Code"]
            output["title"] = row["Title"]

            result = {
                "ug": row["UG"],
                "gd": row["GD"],
                "dk": row["DK"],
                "ng": row["NG"],
                "cpe": row["CPE"],
                "demand": row["Demand"],
                "vacancy": row["Vacancy"],
                "successful_main": row["Successful_Main"],
                "successful_reserve": row["Successful_Reserve"],
                "quota_exceeded": row["Quota_Exceeded"],
                "timetable_clashes": row["Timetable_Clashes"],
                "workload_exceeded": row["Workload_Exceeded"],
                "others": row["Others"],
            }

            # Logic to pad skipped rounds with blanks to ensure that
            # the list stays at the correct length, corresponding to each round.
            if CLASSNAME in class_dict:
                class_dict[CLASSNAME].extend(
                    [BLANK for _
                     in range(index - len(class_dict[CLASSNAME]))])
                class_dict[CLASSNAME].append(result)
            else:
                class_dict[CLASSNAME] = [BLANK] * index
                class_dict[CLASSNAME].append(result)

    # Final padding of classes that don't have all the round information
    for key in class_dict:
        class_dict[key] += [BLANK] * (len(round_numbers) - len(class_dict[key]))

    # If nothing was found, throw an error.
    if not class_dict:
        error_msg = f"Course {code} not found."
        raise ValueError(error_msg)

    # close the database connection if it was created here
    if conn is not None and conn.close is None:
        conn.close()

    return output


def _get_set_of_all_codes(year: Union[str, int],
                          semester: Union[str, int],
                          ug_gd: str,
                          conn: Union[sqlite3.Connection, None] = None,
                          ) -> set[str]:
    """
    Get the set of all known course codes satisfying the arguments.

    Args:
    ----
        year (Union[str, int]): The academic year.
        semester (Union[str, int]): The semester.
        ug_gd (str): The undergraduate/graduate indicator.
        conn (Optional[sqlite3.Connection]):
            Optional database connection object.

    Returns:
    -------
        set[str]: A set of course codes.
    """
    # Clean arguments
    year = _clean_year(year)
    semester = _clean_semester(semester)
    ug_gd = _clean_ug_gd(ug_gd)

    codes: set[str] = set()

    # Establish the database connection if not provided
    if conn is None:
        conn = sqlite3.connect(Path(BASE_DIR) / "database.db")
    conn.row_factory = sqlite3.Row

    # for each round, execute the SQL query
    round_numbers = get_round_numbers(year)
    for round_number in round_numbers:
        TABLE_NAME = (
            "src_history_merged_"
            f"{year}_{semester}_{ug_gd}_round_{round_number}")

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
            codes.add(row["Code"])

    # close the database connection if it was created here
    if conn is not None and conn.close is None:
        conn.close()

    # If nothing was found, throw an error.
    if not codes:
        error_msg = "Data not found."
        raise ValueError(error_msg)

    return codes


@functools.lru_cache
def get_all_data(year: Union[str, int],
                 semester: Union[str, int],
                 ug_gd: str) -> list[CourseData]:
    """
    Get data for all courses satisfying the arguments.

    It will be in the form of a list of course data.
    Each element will be in the form of the output from get_data().

    Args:
    ----
        year (Union[str, int]): The academic year.
        semester (Union[str, int]): The semester.
        ug_gd (str): The undergraduate/graduate indicator.

    Returns:
    -------
        list[CourseData]: A list of course data.
    """
    conn = sqlite3.connect(Path(BASE_DIR) / "database.db")

    codes: set[str] = _get_set_of_all_codes(year, semester, ug_gd, conn)
    sorted_codes: list[str] = sorted(codes)

    output = [get_data(year, semester, ug_gd, code, conn)
              for code in sorted_codes]

    conn.close()

    return output


def _get_filepath(year: Union[str, int],
                  semester: Union[str, int],
                  student_type: str,
                  round_num: Union[str, int],
                  data_folder: str,
                  ext: str) -> Path:
    """
    Generate the absolute file path for a specific file.

    Args:
    ----
        year (Union[str, int]): The year of the file.
        semester (Union[str, int]): The semester of the file.
        student_type (str): The student type of the file.
        round_num (Union[str, int]): The round number of the file.
        data_folder (str): The data folder name where the file is located.
            It refers to the folder in `data/`, such as `data/pdfs`.
        ext (str): The file extension, such as `.csv` or `.pdf`.

    Returns:
    -------
        Path: The absolute file path.
    """
    return (Path(BASE_DIR)
            / "coursereg_history"
            / "data"
            / data_folder
            / str(year)
            / str(semester)
            / student_type
            / f"round_{round_num}.{ext}")


def get_pdf_filepath(year: Union[str, int],
                     semester: Union[str, int],
                     student_type: str,
                     round_num: Union[str, int]) -> Path:
    """
    Generate the absolute file path for a specific PDF file.

    Args:
    ----
        year (Union[str, int]): The year of the PDF file.
        semester (Union[str, int]): The semester of the PDF file.
        student_type (str): The student type of the PDF file.
        round_num (Union[str, int]): The round number of the PDF file.

    Returns:
    -------
        str: The absolute file path of the PDF file.
    """
    return _get_filepath(year, semester, student_type, round_num, "pdfs", "pdf")


def pdf_exists(year: Union[str, int],
               semester: Union[str, int],
               student_type: str,
               round_num: Union[str, int]) -> bool:
    """
    Check if a specific PDF file exists.

    Args:
    ----
        year (Union[str, int]): The year of the PDF file.
        semester (Union[str, int]): The semester of the PDF file.
        student_type (str): The student type of the PDF file.
        round_num (Union[str, int]): The round number of the PDF file.

    Returns:
    -------
        bool: True if and only if the PDF file exists.
    """
    return Path.is_file(get_pdf_filepath(year, semester, student_type, round_num))


def get_latest_year_and_sem_with_data() -> tuple[str, str]:
    """
    Returns the latest year/sem that has coursereg PDF data.

    Returns
    -------
        tuple[str, str]: Tuple containing (acad year, sem).
    """
    cur_year = datetime.now().year

    def get_acad_year_starting_this_calendar_year(cur_year: int) -> str:
        """
        Returns the later AY starting in cur_year.
        If cur_year is 2024, then it returns "2425".

        Returns
        -------
            str: Later AY starting in current year.
        """
        last_two_digits = str(cur_year)[-2:]
        last_two_digits_next_year = str(cur_year + 1)[-2:]

        return last_two_digits + last_two_digits_next_year

    cur_sem = 2
    # Assumption: If UG Round 1 data exists, then that AY+Sem can be displayed.
    while not pdf_exists(
            get_acad_year_starting_this_calendar_year(cur_year),
            cur_sem,
            "ug",
            1,
    ):
        if cur_sem == 2:
            cur_sem -= 1
        else:
            cur_year -= 1
            cur_sem = 2

    latest_year = get_acad_year_starting_this_calendar_year(cur_year)
    latest_sem = str(cur_sem)
    return (latest_year, latest_sem)
