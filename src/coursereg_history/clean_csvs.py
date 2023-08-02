import argparse
import csv
import os
from typing import List

INF = 2147483647


def _clean(s: str) -> str:
    """
    Helper function which strips extraneous whitespaces
    and removes leading and trailing whitespaces.
    It also replaces \n and \r with a saner ' '.

    Args:
        s (str): The input string/int to clean.

    Returns:
        str: The cleaned string.
    """
    s = ' '.join(s.split())
    s = s.replace('\n', ' ')
    s = s.replace('\r', ' ')
    s = s.strip()
    return s


def _add_inf_to_data(data: List[List[str]]) -> None:
    """
    Helper function which takes in cleaned data and makes the
    vacancy sane.
    If the vacancy is empty or a '-', then it implies it has infinite
    vacancy and should be replaced with a big integer, i.e. INF.

    Args:
        data (List[List[str]]): The cleaned data to add INF to.

    Returns:
        None
    """
    # 5 corresponds to vacancy
    for row in data:
        if row[5] == '-' or row[5] == '':
            row[5] = str(INF)


def _clean_row(r: List[str]) -> List[str]:
    """
    Helper function which takes in a CSV row and cleans
    each entry in the row.

    - New lines turn into normal spaces
    - If "-" is found in the data, we replace it with a large number INF.
    - We also strip whitespaces with the clean() function.

    Args:
        r (List[str]): The list of data to clean.

    Returns:
        List[str]: The cleaned list.
    """
    r = [_clean(item) for item in r]
    return r


def _is_overflowed_row(row: List[str]) -> bool:
    """
    Helper function which detects obviously misbehaving rows,
    particularly anything with missing data.

    Args:
        row (List[str]): A row in the course data.

    Returns:
        bool: True iff the row is invalid.
    """
    return all(item == '' for item in row[-8:])


def _is_header_row(row: List[str]) -> bool:
    """
    Helper function which removes obviously unimportant information,
    particularly the headers of the tables.

    Args:
        row (List[str]): A row in the course data.

    Returns:
        bool: True iff the row is a header row.
    """
    HEADER_ROWS: List[List[str]] = [
            ['Module Host Faculty/School', 'Module Host Department',
             'Module Code', 'Module Title', 'Module Class', 'Vacancy',
             'Demand', 'Successful Allocations',
             'Unsuccessful Allocations due to:', '', '', '', ''],
            ['Course Host Faculty/School', 'Course Host Department',
             'Course Code', 'Course Title', 'Course Class', 'Vacancy',
             'Demand', 'Successful Allocations',
             'Unsuccessful Allocations due to:', '', '', '', ''],
            ['', '', '', '', '', '', '', 'Main List', 'Reserve List',
             'Quota Exceeded', 'Timetable Clashes',
             'Workload Exceeded', 'Others'],
            ['', '', '', '', '', '', 'Main List', 'Reserve List',
             'Quota Exceeded', 'Timetable Clashes',
             'Workload Exceeded', 'Others', '']
            ]
    return row in HEADER_ROWS


def _merge_overflowed_rows(data: List[List[str]]) -> List[List[str]]:
    """
    Given data of which all rows contain useful information,
    misbehaving rows are a result of the course overflowing from the
    previous page.
    They must be merged with the previous row, combining 2 rows
    into 1 row of course information.

    Args:
        data (List[List[str]]): The filtered data of useful information.

    Returns:
        List[List[str]]: The merged data.
    """
    merged_data: List[List[str]] = []

    i = 0
    while i < len(data):
        curr_row = data[i]
        next_row = data[i + 1] if i + 1 < len(data) else None

        if next_row is not None and _is_overflowed_row(next_row):
            # Merge the next row with the current element-wise.
            merged_row = [_clean(curr_row[col] + '\n' + next_row[col])
                          for col in range(len(curr_row))]
            merged_data.append(merged_row)
            i += 2
        else:
            merged_data.append(curr_row)
            i += 1

    return merged_data


def _insert_header(data: List[List[str]], header: List[str]) -> None:
    """
    Insert a header row in front of the data set.
    This is to label the columns.

    Args:
        data (List[List[str]]): The cleaned data.
        header (List[List[str]]): The header row to insert
        in front of the data.

    Returns:
        None
    """
    data.insert(0, header)


def _write_to_csv(data: List[List[str]], output_file_path: str) -> None:
    """
    Write a list of rows containing the data to a csv.

    Args:
        data (List[List[str]]): The cleaned data to write.
        output_file_path (str): The path to save the cleaned CSV file.

    Returns:
        None
    """
    with open(output_file_path, 'w', newline='\n') as f:
        writer = csv.writer(f)
        for row in data:
            writer.writerow(row)


def clean_csv(input_file_path: str, output_file_path: str) -> None:
    """
    Clean a CSV file containing raw Tabula'd data.
    We first filter out bad rows, then merge overflowed rows.

    Args:
        input_file_path (str): The path to the input CSV file.
        output_file_path (str): The path to save the cleaned CSV file.

    Returns:
        None
    """
    with open(input_file_path, 'r') as f:
        data: List[List[str]] = list(csv.reader(f))

    data = [_clean_row(row) for row in data]
    data = [row for row in data if not _is_header_row(row)]
    data = _merge_overflowed_rows(data)
    _add_inf_to_data(data)
    _insert_header(data,
                   ["Faculty", "Department", "Code", "Title", "Class",
                    "Vacancy", "Demand",
                    "Successful (Main)", "Successful (Reserve)",
                    "Quota Exceeded", "Timetable Clashes", "Workload Exceeded",
                    "Others"])

    _write_to_csv(data, output_file_path)


def main() -> None:
    parser = argparse.ArgumentParser(description='CSV Cleaner')
    parser.add_argument('--input', '-i',
                        help='Input CSV files', required=True, nargs='+')
    args = parser.parse_args()

    # For each input file, clean the file and generate output
    for input_file in args.input:
        # generate the output file path
        output_file = input_file.replace("raw", "cleaned")

        # Create the output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        clean_csv(input_file, output_file)


if __name__ == "__main__":
    main()
