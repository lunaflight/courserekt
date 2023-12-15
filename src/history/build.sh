time python src/history/convert_pdfs.py src/history/vacancy_history/data/pdfs/*/*/*.pdf src/history/coursereg_history/data/pdfs/*/*/*/*.pdf
python src/history/vacancy_history/clean_csvs.py -i src/history/vacancy_history/data/raw/*/*/*.csv
python src/history/coursereg_history/clean_csvs.py -i src/history/coursereg_history/data/raw/*/*/*/*.csv
python src/history/import_csv_to_db.py src/history/vacancy_history/data/cleaned/*/*/*.csv src/history/coursereg_history/data/cleaned/*/*/*/*.csv
python src/history/merge_db.py src/history/coursereg_history/data/cleaned/*/*/*/*.csv
