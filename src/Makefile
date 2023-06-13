# Find all PDFs
PDFS = $(shell find data/pdfs -name "*.pdf")

# All PDFs will generate a corresponding CSV in data/raw
RAW_CSVS = $(patsubst data/pdfs/%.pdf,data/raw/%.csv,$(PDFS))

# All RAW_CSVS will generate a corresponding CSV in data/cleaned
CLEANED_CSVS = $(patsubst data/raw/%.csv,data/cleaned/%.csv,$(RAW_CSVS))

# By default, build the database
.PHONY: all
all: database.db

# Build the database from all cleaned CSVs
database.db: $(CLEANED_CSVS)
	python csv_to_db.py $^

# Clean CSVs are built from raw CSVs
$(CLEANED_CSVS): data/cleaned/%.csv: data/raw/%.csv
	python clean_csvs.py -i $<

# Raw CSVs are built from PDFs
$(RAW_CSVS): data/raw/%.csv: data/pdfs/%.pdf
	./convert_pdfs $<
