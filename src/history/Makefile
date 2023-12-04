# Find all PDFs
PDFS = $(shell find coursereg_history/data/pdfs -name "*.pdf")

# All PDFs will generate a corresponding CSV in data/raw
RAW_CSVS = $(patsubst coursereg_history/data/pdfs/%.pdf,coursereg_history/data/raw/%.csv,$(PDFS))

# All RAW_CSVS will generate a corresponding CSV in data/cleaned
CLEANED_CSVS = $(patsubst coursereg_history/data/raw/%.csv,coursereg_history/data/cleaned/%.csv,$(RAW_CSVS))

# By default, build the database
.PHONY: all
all: database.db

# Build the database from all cleaned CSVs
database.db: $(CLEANED_CSVS)
	python csv_to_db.py $^

# Clean CSVs are built from raw CSVs
$(CLEANED_CSVS): coursereg_history/data/cleaned/%.csv: coursereg_history/data/raw/%.csv
	python coursereg_history/clean_csvs.py -i $<

# Raw CSVs are built from PDFs
$(RAW_CSVS): coursereg_history/data/raw/%.csv: coursereg_history/data/pdfs/%.pdf
	convert_pdfs $<
