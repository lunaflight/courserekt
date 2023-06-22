from src.planner.Scheduler import Scheduler
from src.planner.nusmods_api import class_type_to_abbr, get_data
import json


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


def backtrack(scheduler, classes, index=0, results=[]):
    if index == len(classes):
        return True

    for class_no, timeslots in classes[index]['info'].items():
        if (allocate(scheduler, timeslots)):
            if (backtrack(scheduler, classes, index + 1, results)):
                results.append({'course_code': classes[index]["course_code"],
                                'timeslots': timeslots})
                return True
            else:
                deallocate(scheduler, timeslots)

    return False


def remove_timings(data):
    for classes in data.values():
        for myclass in classes:
            myclass['startTime'] = '0000'
            myclass['endTime'] = '0000'
    return data


def get_valid_from_json(timetables, whitelist):
    arr = []
    for course_code, classes in timetables.items():
        for class_type, data in classes.items():
            if course_code in whitelist and class_type_to_abbr(class_type) in whitelist[course_code]:
                data = remove_timings(data)

            class_info = {
                    "course_code": course_code,
                    "class_type": class_type,
                    "choices": len(data),
                    "info": data
                    }
            arr.append(class_info)

    sorted_arr = sorted(arr, key=lambda x: x["choices"])
    scheduler = Scheduler()
    results = []
    if (backtrack(scheduler, sorted_arr, 0, results)):
        return results
    else:
        return None


def get_valid(acad_year, semester_no, modules, whitelist):
    data = get_data(acad_year, semester_no, modules)
    return get_valid_from_json(data, whitelist)


def main():
    acad_year = '2022-2023'  # Change to current academic year
    semester_no = 1  # Change to current semester
    modules = ['CS2100']  # Add your modules here

    print(json.dumps(get_valid(acad_year, semester_no, modules), indent=2))


if __name__ == "__main__":
    main()
