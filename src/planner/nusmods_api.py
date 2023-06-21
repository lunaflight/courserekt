import requests
import json


def class_type_to_abbr(class_type: str) -> str:
    # https://github.com/nusmodifications/nusmods/blob/22776c45ab16e85d5ee8a8c900c1a3ca34f44d7b/website/src/utils/timetables.ts#L64
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


def get_module_data(acad_year, module_code):
    url = f"https://api.nusmods.com/v2/{acad_year}/modules/{module_code}.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for module {module_code}")
        return None


def get_module_timetable(acad_year, semester_no, module_code):
    module_data = get_module_data(acad_year, module_code)
    try:
        semesters = module_data['semesterData']
        for semester in semesters:
            if semester['semester'] == semester_no:
                return semester
        return module_data['timetable']
    except AttributeError:
        return None


def get_formatted_timetable(acad_year, semester_no, module_code):
    timetable = get_module_timetable(acad_year, semester_no, module_code)
    if timetable is None:
        return None

    schedule_candidates = {}

    for lesson in timetable['timetable']:
        lessonType = lesson['lessonType']
        classNo = lesson['classNo']

        # If the key is not in the dictionary yet, add it with an empty list as value
        if lessonType not in schedule_candidates:
            schedule_candidates[lessonType] = {}

        if classNo not in schedule_candidates[lessonType]:
            schedule_candidates[lessonType][classNo] = []

        # Append the current lesson to the list of lessons for the key
        schedule_candidates[lessonType][classNo].append(lesson)

    return schedule_candidates


def get_data(acad_year, semester_no, courses):
    timetables = {}

    for module_code in courses:
        timetables[module_code] = (
                get_formatted_timetable(acad_year, semester_no, module_code))

    return timetables


def main():
    acad_year = '2022-2023'  # Change to current academic year
    semester_no = 2  # Change to current semester
    modules = ['HSI1000', 'EL2101', 'LAJ3202', 'ES2660']  # Add your modules here

    print(json.dumps(get_data(acad_year, semester_no, modules), indent=4))


if __name__ == "__main__":
    main()
