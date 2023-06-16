import sqlite3
import pandas as pd
import argparse
import os

# Set up command-line argument parsing
parser = argparse.ArgumentParser(description='Process some CSV files.')
parser.add_argument('csv_files', metavar='N', type=str, nargs='+',
                    help='CSV files to be processed')

args = parser.parse_args()

# Connect to your SQLite database
conn = sqlite3.connect('database.db')

# Process each CSV file
for csv_file in args.csv_files:
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
