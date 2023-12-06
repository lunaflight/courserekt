import sqlite3
from typing import List
import argparse
import os


def merge_csv_files(csv_files: List[str]) -> None:
    """
    Given a list of CourseReg History cleaned files,
    after having imported all relevant CSVs,
    attempt to merge them with useful Vacancy Histories.
    """

    conn = sqlite3.connect('separated_database.db')

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

        conn.execute(f"""
            CREATE TABLE {name} AS
            SELECT
              COALESCE(vacancy.Faculty, coursereg.Faculty) AS Faculty,
              COALESCE(vacancy.Code, coursereg.Code) AS Code,
              COALESCE(vacancy.Title, coursereg.Title) AS Title,
              COALESCE(vacancy.Class, coursereg.Class) AS Class,
              vacancy.UG AS UG,
              vacancy.GD AS GD,
              vacancy.DK AS DK,
              vacancy.NG AS NG,
              vacancy.CPE AS CPE,
              coursereg.Vacancy,
              coursereg.Demand,
              coursereg.Successful_Main AS Successful_Main,
              coursereg.Successful_Reserve AS Successful_Reserve,
              coursereg.Quota_Exceeded AS Quota_Exceeded,
              coursereg.Timetable_Clashes AS Timetable_Clashes,
              coursereg.Workload_Exceeded AS Workload_Exceeded,
              coursereg.Others AS Others
            FROM
              (
                SELECT *
                FROM {vacancy_name}
                WHERE {"UG" if is_ug else "GD"} != 'x'
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
