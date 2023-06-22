import requests
import json
from typing import Any, Dict, List, Union


def class_type_to_abbr(class_type: str) -> str:
    """This function converts the known class types to the standardised
    abbreviations as per the following link.
    https://github.com/nusmodifications/nusmods/blob/22776c45ab16e85d5ee8a8c900c1a3ca34f44d7b/website/src/utils/timetables.ts#L64
    """
    abbr_dict = {
            'Design Lecture': 'DLEC',
            'Laboratory': 'LAB',
            'Lecture': 'LEC',
            'Packaged Lecture': 'PLEC',
            'Packaged Tutorial': 'PTUT',
            'Recitation': 'REC',
            'Sectional Teaching': 'SEC',
            'Seminar-Style Module Class': 'SEM',
            'Tutorial': 'TUT',
            'Tutorial Type 2': 'TUT2',
            'Tutorial Type 3': 'TUT3',
            'Workshop': 'WS',
            }
    return abbr_dict[class_type]


def get_module_data(acad_year: Union[str, int],
                    module_code: str) -> Dict[str, Any]:
    """This function queries the API for the information of this specific course.
    Refer to the following link for more information.
    https://api.nusmods.com/v2/
    """
    url = f"https://api.nusmods.com/v2/{acad_year}/modules/{module_code}.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError("Invalid course code "
                         f"{acad_year}:{module_code} found.")


def get_module_timetable(acad_year: Union[str, int],
                         semester_no: int,
                         module_code: str) -> Dict[str, Any]:
    """This function attempts to fetch the information of the course
    for only the given semester."""
    module_data = get_module_data(acad_year, module_code)

    try:
        semesters = module_data['semesterData']
        for semester in semesters:
            if semester['semester'] == semester_no:
                return semester
        return module_data['timetable']
    except KeyError:
        raise ValueError(f"Could not find {module_code} "
                         f"in semester {semester_no}")


CourseCandidates = Dict[str, Dict[str, List[Dict[str, Any]]]]


def get_formatted_timetable(acad_year: Union[str, int],
                            semester_no: int,
                            module_code: str) -> CourseCandidates:
    """This function takes in a course, the year and semester,
    and returns a Dictionary. This dictionary is keyed first by
    the type of class, for example, "Tutorial".
    Then, it is keyed by the class number, for example, "G05".
    Then, a list is returned of all the classes, as per the API format."""
    timetable = get_module_timetable(acad_year, semester_no, module_code)

    schedule_candidates: CourseCandidates = {}

    for lesson in timetable['timetable']:
        lessonType = lesson['lessonType']
        classNo = lesson['classNo']

        # If the key is not in the dictionary yet,
        # add it with an empty list as value
        if lessonType not in schedule_candidates:
            schedule_candidates[lessonType] = {}

        if classNo not in schedule_candidates[lessonType]:
            schedule_candidates[lessonType][classNo] = []

        # Append the current lesson to the list of lessons for the key
        schedule_candidates[lessonType][classNo].append(lesson)

    return schedule_candidates


def get_data(acad_year: Union[str, int],
             semester_no: int,
             courses: List[str]) -> Dict[str, CourseCandidates]:
    """This function takes in a list of courses, and returns the
    candidates as per get_formatted_timetable(), in a dictionary
    keyed by the course names."""
    timetables = {}

    for module_code in courses:
        timetable = (
                get_formatted_timetable(acad_year, semester_no, module_code))

        timetables[module_code] = timetable
    return timetables


def main() -> None:
    acad_year = '2022-2023'
    semester_no = 2
    modules = ['HSI1000', 'EL2101', 'LAJ3202', 'ES2660']

    print(json.dumps(get_data(acad_year, semester_no, modules), indent=4))


if __name__ == "__main__":
    main()
