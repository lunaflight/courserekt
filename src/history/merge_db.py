import sqlite3
from typing import List
import argparse
import os

NA = -1


def merge_csv_files(csv_files: List[str]) -> None:
    """
    Given a list of CourseReg History cleaned files,
    after having imported all relevant CSVs,
    attempt to merge them with useful Vacancy Histories.
    """

    conn = sqlite3.connect('database.db')

    for csv_file in csv_files:
        # Given name of CourseReg:
        # coursereg_history_data_cleaned_2324_1_ug_round_0
        coursereg_name = os.path.splitext(csv_file)[0].replace('/', '_')

        is_ug: bool = "_ug_" in coursereg_name

        # Corresponding name of Vacancy:
        # vacancy_history_data_cleaned_2324_1_round_0
        vacancy_name = (coursereg_name.replace("coursereg_history_",
                                               "vacancy_history_")
                                      .replace("_ug_", "_")
                                      .replace("_gd_", "_"))

        # Corresponding name of Merged: merged_2324_1_ug_round_0
        name = coursereg_name.replace("coursereg_history_data_cleaned_",
                                      "merged_")

        conn.execute(f"DROP TABLE IF EXISTS \"{name}\"")

        conn.execute(f"""
            CREATE TABLE {name} AS
            SELECT
              COALESCE(vacancy.Faculty, coursereg.Faculty) AS Faculty,
              COALESCE(vacancy.Department, coursereg.Department) AS Department,
              COALESCE(vacancy.Code, coursereg.Code) AS Code,
              COALESCE(vacancy.Title, coursereg.Title) AS Title,
              COALESCE(vacancy.Class, coursereg.Class) AS Class,
              vacancy.UG AS UG,
              vacancy.GD AS GD,
              vacancy.DK AS DK,
              vacancy.NG AS NG,
              vacancy.CPE AS CPE,
              COALESCE(coursereg.Vacancy, vacancy.{"UG" if is_ug else "GD"}) AS Vacancy,
              COALESCE(coursereg.Demand, 0) AS Demand,
              COALESCE(coursereg.Successful_Main, 0) AS Successful_Main,
              COALESCE(coursereg.Successful_Reserve, 0) AS Successful_Reserve,
              COALESCE(coursereg.Quota_Exceeded, 0) AS Quota_Exceeded,
              COALESCE(coursereg.Timetable_Clashes, 0) AS Timetable_Clashes,
              COALESCE(coursereg.Workload_Exceeded, 0) AS Workload_Exceeded,
              COALESCE(coursereg.Others, 0) AS Others
            FROM
              (
                SELECT *
                FROM {vacancy_name}
                WHERE {"UG" if is_ug else "GD"} != '{NA}'
              ) AS vacancy
            FULL JOIN
              {coursereg_name} as coursereg
            ON
              vacancy.Code = coursereg.Code
            AND
              vacancy.Class = coursereg.Class;
        """)

    conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(description='Merge some CSV files.')
    parser.add_argument('csv_files', metavar='N', type=str, nargs='+',
                        help='CSV files to be merged')

    args = parser.parse_args()

    merge_csv_files(args.csv_files)


if __name__ == "__main__":
    main()
