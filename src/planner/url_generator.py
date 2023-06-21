from planner.valid_timetable_finder import get_valid
from planner.nusmods_api import class_type_to_abbr


def generate_syntax(acad_year, semester, courses, whitelist):
    choices = get_valid(acad_year, semester, courses, whitelist)
    if choices is None:
        return None

    course_choices = {}

    for choice in choices:
        CODE = choice['course_code']
        ABBR = class_type_to_abbr(choice['timeslots'][0]['lessonType'])
        CLASS_NO = choice['timeslots'][0]['classNo']

        if CODE not in course_choices:
            course_choices[CODE] = []

        course_choices[CODE].append(f"{ABBR}:{CLASS_NO}")

    syntaxes = []
    for code, class_syntaxes in course_choices.items():
        syntaxes.append(f"{code}={','.join(class_syntaxes)}")

    return '&'.join(syntaxes)


def generate_url(acad_year, semester, courses, whitelist):
    syntax = generate_syntax(acad_year, semester, courses, whitelist)
    if syntax is None:
        return None

    return f"https://nusmods.com/timetable/sem-{semester}/share?{syntax}"


def main():
    acad_year = '2022-2023'  # Change to current academic year
    semester_no = 1  # Change to current semester
    modules = ['LAJ2201', 'CS2100', 'ST2334', 'CS2106', 'CS2107', 'CS2109S', 'LAJ3201', 'CS2102', 'CS2103T', 'CS2105', 'CS3230', 'CS3241', 'LAJ3202', 'EL2102']  # Add your modules here
    whitelist = {
            "CS2100": ["REC"]
            }
    # modules = ['CS2100']
    print(generate_url(acad_year, semester_no, modules, whitelist))


if __name__ == "__main__":
    main()
