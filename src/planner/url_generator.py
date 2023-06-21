from valid_timetable_finder import get_valid


def class_type_to_abbr(class_type):
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


def generate_syntax(acad_year, semester, courses):
    choices = get_valid(acad_year, semester, courses)
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


def generate_url(acad_year, semester, courses):
    syntax = generate_syntax(acad_year, semester, courses)
    if syntax is None:
        return None

    return f"https://nusmods.com/timetable/sem-{semester}/share?{syntax}"


def main():
    acad_year = '2022-2023'  # Change to current academic year
    semester_no = 1  # Change to current semester
    modules = ['CS2102', 'CS2103T', 'CS2105', 'CS3230', 'CS3241', 'LAJ3202', 'EL2102']  # Add your modules here
    # modules = ['CS2100']
    print(generate_url(acad_year, semester_no, modules))


if __name__ == "__main__":
    main()
