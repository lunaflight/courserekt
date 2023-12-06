import sqlite3
from typing import List
import pandas as pd
import argparse
import os


def process_csv_files(csv_files: List[str]) -> None:
    """Processes a list of CSV files by loading them
    into an SQLite database."""

    # Connect to your SQLite database
    conn = sqlite3.connect('database.db')

    # Process each CSV file
    for csv_file in csv_files:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(csv_file)

        # Get the name of the table from the filename
        table_name = os.path.splitext(csv_file)[0].replace('/', '_')

        # Drop the existing table (if it exists)
        conn.execute(f"DROP TABLE IF EXISTS \"{table_name}\"")

        # Write the data from your DataFrame into the database
        df.to_sql(table_name, conn, index=False)

    # Don't forget to close the connection when you're done
    conn.close()


def main() -> None:
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Process some CSV files.')
    parser.add_argument('csv_files', metavar='N', type=str, nargs='+',
                        help='CSV files to be processed')

    args = parser.parse_args()

    process_csv_files(args.csv_files)


if __name__ == "__main__":
    main()
