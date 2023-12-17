import subprocess

# Define script paths
convert_pdfs_script = "src/history/convert_pdfs.py"
clean_vh_csvs_script = "src/history/vacancy_history/clean_csvs.py"
clean_crh_csvs_script = "src/history/coursereg_history/clean_csvs.py"
import_csv_to_db_script = "src/history/import_csv_to_db.py"
merge_db_script = "src/history/merge_db.py"

# Define input directories
vh_pdfs_glob = "src/history/vacancy_history/data/pdfs/*/*/*.pdf"
crh_pdfs_glob = "src/history/coursereg_history/data/pdfs/*/*/*/*.pdf"
vh_raw_csvs_glob = "src/history/vacancy_history/data/raw/*/*/*.csv"
crh_raw_csvs_glob = "src/history/coursereg_history/data/raw/*/*/*/*.csv"
vh_cleaned_csvs_glob = "src/history/vacancy_history/data/cleaned/*/*/*.csv"
crh_cleaned_csvs_glob = "src/history/coursereg_history/data/cleaned/*/*/*/*.csv"

# Convert PDFS
subprocess.run(f"time python {convert_pdfs_script} {vh_pdfs_glob} {crh_pdfs_glob}", shell=True)

# Clean vacancy history CSV files
subprocess.run(f"python {clean_vh_csvs_script} -i {vh_raw_csvs_glob}", shell=True)

# Clean course registration history CSV files
subprocess.run(f"python {clean_crh_csvs_script} -i {crh_raw_csvs_glob}", shell=True)

# Import CSV files to database
subprocess.run(f"python {import_csv_to_db_script} {vh_cleaned_csvs_glob} {crh_cleaned_csvs_glob}", shell=True)

# Merge database tables
subprocess.run(f"python {merge_db_script} {crh_cleaned_csvs_glob}", shell=True)

print("Build process completed!")
