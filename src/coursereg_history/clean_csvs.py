import argparse
import csv
import os
import pandas as pd
import re
from typing import Iterator, List, Union

INF = 2147483647
COURSE_REGEX = r'[A-Z]{2,5}\d{4}[A-Z]?'


def clean_csv(input_file_path: str, output_file_path: str) -> None:
    # Define the column headers for our pandas DataFrame
    cols = ["Faculty", "Department", "Code", "Title", "Class",
            "Vacancy", "Demand",
            "Successful (Main)", "Successful (Reserve)",
            "Quota Exceeded", "Timetable Clashes", "Workload Exceeded",
            "Others"]
    COL_COUNT = 13
    dtypes = {"Vacancy": int, "Demand": int, "Successful (Main)": int,
              "Successful (Reserve)": int, "Quota Exceeded": int,
              "Timetable Clashes": int, "Workload Exceeded": int,
              "Others": int}

    # Instantiate an empty DataFrame with our column headers
    df = pd.DataFrame(columns=cols).astype(dtypes)

    # Define a helper function to clean up and normalize our string data
    def clean(s: Union[str, int]) -> str:
        s = str(s)
        # Remove extraneous whitespace and trim leading/trailing spaces
        return (' '.join(s.split())).strip()

    def clean_row(r: List[str]) -> List[str]:
        r = [item.replace('\n', ' ') for item in r]
        r = [str(INF) if item == '-' else item for item in r]
        return [clean(item) for item in r]

    # Open our raw data CSV file and read it into a list
    with open(input_file_path, 'r') as f:
        data = list(csv.reader(f))

    # Define our padding rows, to be used for ensuring we can iterate safely
    padding_start = [['' for _ in range(COL_COUNT)]]
    padding_end = [['' for _ in range(COL_COUNT)] for _ in range(3)]

    # Pad our data at the start and end
    data = padding_start + data + padding_end

    # Define a helper function to create an iterator with
    # a certain number of "skipped" elements
    def iter_with_skip(data: List[List[str]],
                       num_skips: int) -> Iterator[List[str]]:
        it = iter(data)
        for _ in range(num_skips):
            next(it, None)
        return it

    # Create four copies of our iterator,
    # each starting at a different point in the data
    it1 = iter(data)
    it2 = iter_with_skip(data, 1)
    it3 = iter_with_skip(data, 2)
    it4 = iter_with_skip(data, 4)

    # Loop through our data, processing four rows at a time
    for prev_row, row, next_row, nextnextnext_row in zip(it1, it2, it3, it4):
        # Replace newline characters in our row
        row = clean_row(row)

        # Check if the row has the expected
        # number of fields and the right format
        if (len(row) == len(cols) and
            all(cell.isdigit()
                for cell in row[5:])):
            # Edge Case: The course was cut off and continued
            # on the next page - merge with 3 rows in the future.
            if all(cell == '' for cell in nextnextnext_row[5:]):
                new_row = [a + ' ' + b for a, b in zip(row, nextnextnext_row)]
            else:
                new_row = row
            new_row = clean_row(new_row)

            # Append the new row to the dataframe
            temp_df = pd.DataFrame([new_row], columns=cols)
            df = pd.concat([df, temp_df], ignore_index=True)

        # Edge Case: The courses are on the first page and
        # cannot be parsed properly. Info spread across 3 rows - merge around.
        elif (len(row) == 3 and
              re.match(COURSE_REGEX, row[2].split(' ')[0])):
            faculty = clean(f"{prev_row[0]} {row[0]} {next_row[0]}")
            department = clean(f"{prev_row[1]} {row[1]} {next_row[1]}")

            course_parts = row[2].split()
            code = course_parts[0]
            fragmented_title = ' '.join(course_parts[1:-9])
            title = clean(f"{fragmented_title} {prev_row[2]} {next_row[2]}")

            # Append the cleaned and merged fields to the dataframe
            numbers = course_parts[-9:]
            new_row = ([faculty] + [department] + [code]
                       + [title] + numbers)
            new_row = clean_row(new_row)
            if len(new_row) == len(cols):
                temp_df = pd.DataFrame([new_row], columns=cols)
                df = pd.concat([df, temp_df], ignore_index=True)

    # Save our cleaned and structured data to a new CSV file
    df.to_csv(output_file_path, index=False)


def main() -> None:
    # Instantiate the parser
    parser = argparse.ArgumentParser(description='CSV Cleaner')

    # Add long and short argument
    parser.add_argument('--input', '-i',
                        help='Input CSV files', required=True, nargs='+')

    # Parse arguments
    args = parser.parse_args()

    # For each input file, clean the file and generate output
    for input_file in args.input:
        # generate the output file path
        output_file = input_file.replace("raw", "cleaned")

        # Create the output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # clean the csv file
        clean_csv(input_file, output_file)


if __name__ == "__main__":
    main()
