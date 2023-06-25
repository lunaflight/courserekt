import argparse
import re
from src.planner.url_generator import generate_url
from typing import Dict, List, Union


def parse_year(year_str: Union[str, int]) -> str:
    """A helper function to standardise year inputs to a single format
    of YYYY-YYYY.
    YYYY, YY-YY, YY/YY, YYYYYYYY, YYYY-YYYY, YYYY/YYYY are attempted to be
    converted to the unified format."""

    if isinstance(year_str, int):
        year_str = str(year_str)
    # Replace "/" with "-" if present
    year_str = year_str.replace("/", "-")

    # If input is like "2223"
    if len(year_str) == 4:
        year_str = "20" + year_str[:2] + "-" + "20" + year_str[2:]

    # If input is like "22-23"
    elif len(year_str) == 5:
        year_str = "20" + year_str[:2] + "-" + "20" + year_str[3:]

    # If input is like "20222023"
    elif len(year_str) == 8:
        year_str = year_str[:4] + "-" + year_str[4:]

    return year_str


def parse_whitelist(whitelist_str: List[str]) -> Dict[str, List[str]]:
    """A helper function to parse input of the format
    ["CODE:CLASS_TYPE,CLASS_TYPE,..."] to a dictionary of
    { "CODE": [CLASSTYPE, ...] }"""

    whitelist = {}
    for item in whitelist_str:
        key, value = item.split(":")
        whitelist[key.upper()] = (
                [val.strip().upper() for val in value.split(',')])
    return whitelist


def parse_and_generate_url(acad_year: Union[str, int],
                           semester_no: Union[str, int],
                           courses: List[str],
                           whitelist: List[str],
                           dry_run: bool = False) -> str:
    """A helper function to clean all data inputs, and then attempt to
    generate a valid timetable and provide the URL for it."""

    acad_year = parse_year(acad_year)
    # Validate academic year
    if not re.match(r'^(\d{4}-\d{4})$', acad_year):
        raise ValueError("Invalid academic year format. "
                         "Use '2223', '22-23', '22/23', "
                         "'20222023', '2022-2023' or '2022/2023'.")

    # Validate semester number
    if semester_no not in [1, 2, "1", "2"]:
        raise ValueError("Invalid semester number. It must be 1 or 2.")

    # Validate whitelist
    for item in whitelist:
        if not re.match(r'^[A-Za-z0-9_]+:[A-Za-z0-9_,]+$', item):
            raise ValueError("Invalid whitelist format. "
                             "Use 'COURSE_ID:CLASS_TYPE,CLASS_TYPE,...'")

    return generate_url(
            parse_year(acad_year),
            int(semester_no),
            [course.upper() for course in courses],
            parse_whitelist(whitelist),
            dry_run)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate NUSMods URL.")

    parser.add_argument('-y', '--year', type=str, default='2023-2024',
                        help='The academic year, e.g., '
                        '"2022-2023", "22-23", "22/23", "2223".')
    parser.add_argument('-s', '--semester', type=int, required=True,
                        help='The semester number (1 or 2).')
    parser.add_argument('-c', '--courses', type=str, nargs='+', required=True,
                        help='The course codes, e.g., -c "LAJ2201" "CS2100".')
    parser.add_argument('-w', '--whitelist', type=str, nargs='+', default=[],
                        help='The whitelist as a series of "COURSE:TYPE" '
                        'strings, e.g., -w "CS2100:LEC,TUT" "LAJ2201:LEC".')

    args = parser.parse_args()

    try:
        print(parse_and_generate_url(args.year, args.semester,
                                     args.courses, args.whitelist))
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
