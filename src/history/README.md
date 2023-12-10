# Implementation

## Glossary
| Name | Meaning |
| --- | --- |
| CourseReg PDF | Course Class Demand and Allocation Report |
| Vacancy PDF | Course Class Vacancy Report |

## Overall Structure of Folder

This folder contains code which scrapes and cleans data from the PDFs given by NUS, which is then parsed into easier-to-read formats.

1. **PDF Storage:**
 - The CourseReg PDFs are stored in `coursereg_history/data/pdfs/{YEAR}/{SEMESTER}/{UG or GD}/round_{0,1,2,3}.pdf`.
 - The Vacancy PDFs are stored in `vacancy_history/data/pdfs/{YEAR}/{SEMESTER}/round_{0,1,2,3}.pdf`.
2. **PDF Parsing:** The PDFs are parsed using [Tabula](https://github.com/tabulapdf/tabula-java) to produce CSV files in `.../data/raws/...` with the same filepath as where it is stored in `.../data/pdfs/...`.
Java is used for this purpose, and we use a bash script `./convert_pdfs` to facilitate conversion.
3. **Data Cleaning:** The raw CSV files are passed through `clean_csvs.py` to produce clean CSVs in `.../data/cleaned/...` with the same filepath as where it is stored in `...data/raws/...`.
4. **Database Entry:** The cleaned CSVs are added to the `database.db` by passing them through `import_csv_to_db.py`.
6. **Merging CourseReg and Vacancy Info:** The information is reconciled by passing them through `merge_db.py`.
7. **Database Entry:** The cleaned CSVs produced in step 4 are no longer needed and are removed with `import_csv_to_db.py` with a `--clean` flag.
8. **API:** Queries about the courses can be made through the `api.py` file, which executes the relevant SQL queries to retrieve the data.

All of these steps are orchestrated using a Makefile.

## Data Cleaning for CourseReg PDFs
We only outline the procedure for CourseReg PDFs, but the logic for Vacancy PDFs is similar, if not, the same.
The CSV returned by Tabula using the `--lattice` flag is well-behaved. Only the data found in the table lattice is captured.
However, great care must still be taken in `clean_csvs.py` to navigate ill-defined data.

The data has 13 columns, corresponding to the following:

- Faculty, Department, Code, Title, Class,
- Vacancy, Demand,
- Successful_Main, Successful_Reserve
- Quota_Exceeded, Timetable_Clashes, Workload_Exceeded, Others.

We remove all table headers from the data, corresponding to `_is_header_row()` in `clean_csvs.py`.

We also do simple housekeeping such as replacing '\n' with ' '.

We will be left with rows that all necessarily contain useful information.
The following list explains, exhaustively, all ill-behaved data found in the table.

### Courses spilling data across pages
Courses with a sufficiently long field on the last entry of the PDF can have its data spill over to the next page.

This is an example taken from `coursereg_history/data/raw/2223/1/ug/round_0.csv`.

**Row `t + 0`**
```
Yale-NUS College,Yale-NUS College,YSS4206C,Topics in Psychology: The Pursuit of,E1,15,9,9,2,0,0,0,0
```
**Row `t + 1`**
```
"",,,Happiness,,,,,,,,,
```

### Courses which have a missing Vacancy field
Courses, especially prefixed with `LL`, tend to have empty vacancy fields.
This should be treated the same as a `-` field.

This is an example taken from `coursereg_history/data/raw/2223/1/ug/round_1.csv`.
```
Faculty of Law,FoL Dean's Office,LL4002V,Admiralty Law & Practice,E1,,3,3,0,0,0,0,0
```

## Duplicate (Code, Class) for Vacancy PDFs
Interestingly, this only occurs for Vacancy PDFs and not for CourseReg PDFs.
Sometimes, there are duplicate entries for the same code and class, listed under different faculties.
These duplicates must be removed when cleaning them.

These are examples taken from `vacancy_history/data/raw/2223/1/round_0.csv`.

BSN3701:
```
NUS,NUS Enterprise Academy,BSN3701,Technological Innovation,SA1,17,-1,-1,30,3
NUS Business School,Strategy and Policy,BSN3701,Technological Innovation,SA1,17,-1,-1,30,3
```

ST2131:
```
Faculty of Science,Mathematics,ST2131,Probability,L1,200,-1,-1,-1,-1
Faculty of Science,Statistics and Data Science,ST2131,Probability,L1,200,-1,-1,-1,-1
```


## Merging
After parsing both CourseReg and Vacancy PDFs, `merge_db.py` attempts to combine the 2.
1. The primary key we use here is `(Code, Class)`. This will allow us to uniquely identify and merge the 2 tables.
2. We filter out irrelevant rows. That is, rows marked with `x` for the `UG` column, for undergraduate reports should be ignored. This is because that would represent the course being unavailable for undergraduates to be picked. Similar logic will apply for `GD` as well.
3. Some rows may appear in both PDFs, or only appear in 1 PDF. We must make sure that the `Demand` and `Vacancy` is available to be fetched by our API. We sanity check this by doing the following:
If we cannot find a value for the following, replace it with...
 - `Vacancy` = `UG/GD` _(available seats for `UG/GD` in the Vacancy PDF)_
 - `Demand` = `0` _(and all other columns)_
