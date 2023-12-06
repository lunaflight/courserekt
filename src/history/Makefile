COURSEREG_PDFS = $(shell find coursereg_history/data/pdfs -name "*.pdf")
VACANCY_PDFS = $(shell find vacancy_history/data/pdfs -name "*.pdf")

# All PDFs will generate a corresponding CSV in data/raw
RAW_COURSEREG_CSVS = $(patsubst coursereg_history/data/pdfs/%.pdf,coursereg_history/data/raw/%.csv,$(COURSEREG_PDFS))
RAW_VACANCY_CSVS = $(patsubst vacancy_history/data/pdfs/%.pdf,vacancy_history/data/raw/%.csv,$(VACANCY_PDFS))

# All RAW_CSVS will generate a corresponding CSV in data/cleaned
CLEANED_COURSEREG_CSVS = $(patsubst coursereg_history/data/raw/%.csv,coursereg_history/data/cleaned/%.csv,$(RAW_COURSEREG_CSVS))
CLEANED_VACANCY_CSVS = $(patsubst vacancy_history/data/raw/%.csv,vacancy_history/data/cleaned/%.csv,$(RAW_VACANCY_CSVS))

# By default, build the database
.PHONY: all, clean
all: separated_database.db
clean:
	rm -f $(RAW_COURSEREG_CSVS) $(RAW_VACANCY_CSVS) $(CLEANED_COURSEREG_CSVS) $(CLEANED_VACANCY_CSVS) separated_database.db

# Build the database from all cleaned CSVs
separated_database.db: $(CLEANED_COURSEREG_CSVS) $(CLEANED_VACANCY_CSVS)
	python import_csv_to_db.py $^;\
	python merge_db.py $(CLEANED_COURSEREG_CSVS);\
	python import_csv_to_db.py --clean $^;

# Clean CSVs are built from raw CSVs
$(CLEANED_COURSEREG_CSVS): coursereg_history/data/cleaned/%.csv: coursereg_history/data/raw/%.csv
	python coursereg_history/clean_csvs.py -i $<
$(CLEANED_VACANCY_CSVS): vacancy_history/data/cleaned/%.csv: vacancy_history/data/raw/%.csv
	python vacancy_history/clean_csvs.py -i $<

# Raw CSVs are built from PDFs
$(RAW_COURSEREG_CSVS): coursereg_history/data/raw/%.csv: coursereg_history/data/pdfs/%.pdf
	./convert_pdfs $<
$(RAW_VACANCY_CSVS): vacancy_history/data/raw/%.csv: vacancy_history/data/pdfs/%.pdf
	./convert_pdfs $<
