HISTORY_PATH = src/history

DATABASE = $(HISTORY_PATH)/database.db

COURSEREG_PDFS = $(shell find $(HISTORY_PATH)/coursereg_history/data/pdfs -name "*.pdf")
VACANCY_PDFS = $(shell find $(HISTORY_PATH)/vacancy_history/data/pdfs -name "*.pdf")

# All PDFs will generate a corresponding CSV in data/raw
RAW_COURSEREG_CSVS = $(patsubst $(HISTORY_PATH)/coursereg_history/data/pdfs/%.pdf,$(HISTORY_PATH)/coursereg_history/data/raw/%.csv,$(COURSEREG_PDFS))
RAW_VACANCY_CSVS = $(patsubst $(HISTORY_PATH)/vacancy_history/data/pdfs/%.pdf,$(HISTORY_PATH)/vacancy_history/data/raw/%.csv,$(VACANCY_PDFS))

# All RAW_CSVS will generate a corresponding CSV in data/cleaned
CLEANED_COURSEREG_CSVS = $(patsubst $(HISTORY_PATH)/coursereg_history/data/raw/%.csv,$(HISTORY_PATH)/coursereg_history/data/cleaned/%.csv,$(RAW_COURSEREG_CSVS))
CLEANED_VACANCY_CSVS = $(patsubst $(HISTORY_PATH)/vacancy_history/data/raw/%.csv,$(HISTORY_PATH)/vacancy_history/data/cleaned/%.csv,$(RAW_VACANCY_CSVS))

# By default, build the database
.PHONY: all, clean
all: $(DATABASE)
clean:
	rm -f $(RAW_COURSEREG_CSVS) $(RAW_VACANCY_CSVS) $(CLEANED_COURSEREG_CSVS) $(CLEANED_VACANCY_CSVS) $(DATABASE)

# Build the database from all cleaned CSVs
$(DATABASE): $(CLEANED_COURSEREG_CSVS) $(CLEANED_VACANCY_CSVS)
	python $(HISTORY_PATH)/import_csv_to_db.py $^;\
	python $(HISTORY_PATH)/merge_db.py $(CLEANED_COURSEREG_CSVS);\
	python $(HISTORY_PATH)/import_csv_to_db.py --clean $^;

# Clean CSVs are built from raw CSVs
$(CLEANED_COURSEREG_CSVS): $(HISTORY_PATH)/coursereg_history/data/cleaned/%.csv: $(HISTORY_PATH)/coursereg_history/data/raw/%.csv
	python $(HISTORY_PATH)/coursereg_history/clean_csvs.py -i $<
$(CLEANED_VACANCY_CSVS): $(HISTORY_PATH)/vacancy_history/data/cleaned/%.csv: $(HISTORY_PATH)/vacancy_history/data/raw/%.csv
	python $(HISTORY_PATH)/vacancy_history/clean_csvs.py -i $<

# Raw CSVs are built from PDFs
$(RAW_COURSEREG_CSVS): $(HISTORY_PATH)/coursereg_history/data/raw/%.csv: $(HISTORY_PATH)/coursereg_history/data/pdfs/%.pdf
	./$(HISTORY_PATH)/convert_pdfs $<
$(RAW_VACANCY_CSVS): $(HISTORY_PATH)/vacancy_history/data/raw/%.csv: $(HISTORY_PATH)/vacancy_history/data/pdfs/%.pdf
	./$(HISTORY_PATH)/convert_pdfs $<
