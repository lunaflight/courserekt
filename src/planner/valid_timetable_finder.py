from Scheduler import Scheduler
from nusmods_api import get_data


def allocate(scheduler, timeslots, index=0):
    if index == len(timeslots):
        return True

    timeslot = timeslots[index]

    start = timeslot["startTime"]
    end = timeslot["endTime"]
    day = timeslot["day"]
    if (scheduler.add(day, start, end)):
        if (allocate(scheduler, timeslots, index + 1)):
            return True
        else:
            scheduler.clear(day, start, end)
            return False
    else:
        return False


def deallocate(scheduler, timeslots):
    for timeslot in timeslots:
        start = timeslot["startTime"]
        end = timeslot["endTime"]
        day = timeslot["day"]

        scheduler.clear(day, start, end)


def backtrack(scheduler, classes, index=0):
    if index == len(classes):
        return True

    for class_no, timeslots in classes[index]['info'].items():
        if (allocate(scheduler, timeslots)):
            if (backtrack(scheduler, classes, index + 1)):
                print(classes[index]['course_code'], class_no)
                return True
            else:
                deallocate(scheduler, timeslots)

    return False


def get_valid(timetables):
    arr = []
    for course_code, classes in timetables.items():
        for class_type, data in classes.items():
            class_info = {
                    "course_code": course_code,
                    "class_type": class_type,
                    "choices": len(data),
                    "info": data
                    }
            arr.append(class_info)

    sorted_arr = sorted(arr, key=lambda x: x["choices"])
    scheduler = Scheduler()
    if (backtrack(scheduler, sorted_arr)):
        return scheduler
    else:
        return None


def main():
    acad_year = '2022-2023'  # Change to current academic year
    semester_no = 1  # Change to current semester
    modules = ['CS3241', 'LAJ3201', 'ES2660', 'EL1101E']  # Add your modules here

    data = get_data(acad_year, semester_no, modules)
    print(str(get_valid(data)))


if __name__ == "__main__":
    main()
