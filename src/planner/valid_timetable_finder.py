from src.planner.Scheduler import Scheduler
from src.planner.nusmods_api import (
        CourseCandidates, class_type_to_abbr, get_data)
import json
from typing import Any, Dict, List, Optional, Union


def allocate(scheduler: Scheduler,
             timeslots: List[Dict[str, Any]],
             index: int = 0) -> bool:
    """This function attempts to schedule and block out all the timeslots
    associated with the class into the scheduler.
    If it is impossible, no changes will be made to the scheduler, i.e.
    all changes will be reverted.
    It returns true iff all the timeslots have been allocated."""
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


def deallocate(scheduler: Scheduler, timeslots: List[Dict[str, Any]]) -> None:
    """This function attempts to unschedule and unblock out all the timeslots
    associated with the class.
    It is assumed that all timeslots have
    been successfully allocated before."""
    for timeslot in timeslots:
        start = timeslot["startTime"]
        end = timeslot["endTime"]
        day = timeslot["day"]

        scheduler.clear(day, start, end)


def backtrack(scheduler: Scheduler,
              classes: List[Dict[str, Any]],
              index: int = 0,
              results: List[Dict[str, Any]] = []) -> bool:
    """This function attempts to go through every required class we need
    to take, and brute forces a possible combination to make a
    valid timetable."""
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


def remove_timings(data: Dict[str, List[Dict[str, Any]]]) -> (
        Dict[str, List[Dict[str, Any]]]):
    """This function helps resolve conflicts in clashes.
    By passing in a whitelist, if the class type is in the whitelist,
    the timings are removed so classes can be placed in this timeslot
    easily."""
    for classes in data.values():
        for myclass in classes:
            myclass['startTime'] = '0000'
            myclass['endTime'] = '0000'
    return data


def get_valid_from_json(timetables: Dict[str, CourseCandidates],
                        whitelist: Dict[str, List[str]]) -> (
                                Optional[List[Dict[str, Any]]]):
    """This function takes in a bunch of ugly data.
    It then sorts it based on the required classes, appending a length
    field onto it. This allows sorting from few choices to many choices.
    This is the Minimum Remaining Values Heuristic.
    This helps speed up the NP-hard problem of timetable scheduling.
    """
    arr: List[Dict[str, Any]] = []
    for course_code, classes in timetables.items():
        for class_type, data in classes.items():
            if course_code in whitelist and (
                    class_type_to_abbr(class_type) in whitelist[course_code]):
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
    results: List[Dict[str, Any]] = []
    if (backtrack(scheduler, sorted_arr, 0, results)):
        return results
    else:
        return None


def get_valid(acad_year: Union[str, int],
              semester_no: int,
              modules: List[str],
              whitelist: Dict[str, List[str]] = {}) -> List[Dict[str, Any]]:
    """This function takes in the relevant year, semester number, courses and
    whitelist of a user and attempts to find a valid configuration of the
    timetable. It will return a list of classes the algorithm decides
    is best."""
    data = get_data(acad_year, semester_no, modules)
    valid = get_valid_from_json(data, whitelist)
    if valid is None:
        raise RuntimeError("No valid timetable found.")
    else:
        return valid


def main() -> None:
    acad_year = '2022-2023'  # Change to current academic year
    semester_no = 1  # Change to current semester
    modules = ['CS2100']  # Add your modules here

    print(json.dumps(get_valid(acad_year, semester_no, modules), indent=2))


if __name__ == "__main__":
    main()
