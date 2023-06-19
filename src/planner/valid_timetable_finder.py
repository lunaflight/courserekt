import json
from Scheduler import Scheduler


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
    with open('sample.json', 'r') as json_file:
        data = json.load(json_file)
    print(str(get_valid(data)))


if __name__ == "__main__":
    main()
