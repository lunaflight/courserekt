# Implementation

## CourseReg Records

It contains code which scrapes and cleans data from the PDFs given by NUS, which is then parsed into easier-to-read formats.

1. **PDF Storage:** The PDFs are stored in `data/pdfs/{YEAR}/{SEMESTER}/{UG or GD}/round_{0,1,2,3}.pdf`.
2. **PDF Parsing:** The PDFs are parsed using [Tabula](https://github.com/tabulapdf/tabula-java) to produce CSV files in `data/raws/{YEAR}/{SEMESTER}/{UG or GD}/round_{0,1,2,3}.csv`. Java is used for this purpose, and we use a bash script `./convert_pdfs` to facilitate conversion.
3. **Data Cleaning:** The raw CSV files are passed through `clean_csvs.py` to produce clean CSVs in `data/cleaned/{YEAR}/{SEMESTER}/{UG or GD}/round_{0,1,2,3}.csv`.
4. **Database Entry:** The cleaned CSVs are added to the `database.db` by passing them through `csv_to_db.py`.
5. **API:** Queries about the courses can be made through the `api.py` file, which executes the relevant SQL queries to retrieve the data.

All of these steps are orchestrated using a Makefile.

## Data Cleaning
The CSV returned by Tabula using the `--lattice` flag is well-behaved. Only the data found in the table lattice is captured.
However, great care must still be taken in `clean_csvs.py` to navigate ill-defined data.

The data has 13 columns, corresponding to the following:

- Faculty, Department, Code, Title, Class,
- Vacancy, Demand,
- Successful (Main), Successful (Reserve)
- Quota Exceeded, Timetable Clashes, Workload Exceeded, Others.

We remove all table headers from the data, corresponding to `_is_header_row()` in `clean_csvs.py`.

We also do simple housekeeping such as replacing '\n' with ' '.

We will be left with rows that all necessarily contain useful information.
The following list explains, exhaustively, all ill-behaved data found in the table.

### Courses spilling data across pages
Courses with a sufficiently long field on the last entry of the PDF can have its data spill over to the next page.

This is an example taken from `raw/2223/1/ug/round_0.csv`.

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

This is an example taken from `raw/2223/1/ug/round_1.csv`.
```
Faculty of Law,FoL Dean's Office,LL4002V,Admiralty Law & Practice,E1,,3,3,0,0,0,0,0
```

# Usage

## `api.py`

### get_all_data

```python3
def get_all_data(
    year: Union[str, int],
    semester: Union[str, int],
    ug_gd: str
) -> List[Dict[str, Union[str, Dict[str, List[Dict[str, int]]]]]]
```

Get data for all courses in a specific year, semester, and undergraduate/graduate.
It will be in the form of a list of course data.
Each element will be in the form of the output from get_data().

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| year | Union[str, int] | The academic year. | None |
| semester | Union[str, int] | The semester. | None |
| ug_gd | str | The undergraduate/graduate indicator. | None |

**Returns:**

| Type | Description |
|---|---|
| List[CourseData] | A list of course data. |

### get_data

```python3
def get_data(
    year: Union[str, int],
    semester: Union[str, int],
    ug_gd: str,
    code: str,
    conn: Optional[sqlite3.Connection] = None
) -> Dict[str, Union[str, Dict[str, List[Dict[str, int]]]]]
```

Retrieve data for a specific course from the database.

The data is in the format of the following:
```
    'faculty': str,
    'department': str,
    'code': str,
    'title': str,
    'classes': class_dict
```

The class dict has keys of the class name, for example "SG01" (Sectional
teaching group 1). Its value is a list of length 4.

Each element corresponds to the information in round 0, 1, 2 and 3.
They have the following format:
```
    'demand': int,
    'vacancy': int,
    'successful_main': int,
    'successful_reserve': int,
    'quota_exceeded': int,
    'timetable_clashes': int,
    'workload_exceeded': int,
    'others': int,
```

### get_pdf_filepath

```python3
def get_pdf_filepath(
    year: Union[str, int],
    semester: Union[str, int],
    type: str,
    round_num: Union[str, int]
) -> str
```

Generate the absolute file path for a specific PDF file.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| year | Union[str, int] | The year of the PDF file. | None |
| semester | Union[str, int] | The semester of the PDF file. | None |
| type | str | The type of the PDF file. | None |
| round_num | Union[str, int] | The round number of the PDF file. | None |

**Returns:**

| Type | Description |
|---|---|
| str | The absolute file path of the PDF file. |

### pdf_exists

```python3
def pdf_exists(
    year: Union[str, int],
    semester: Union[str, int],
    type: str,
    round_num: Union[str, int]
) -> bool
```

Check if a specific PDF file exists.

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| year | Union[str, int] | The year of the PDF file. | None |
| semester | Union[str, int] | The semester of the PDF file. | None |
| type | str | The type of the PDF file. | None |
| round_num | Union[str, int] | The round number of the PDF file. | None |

**Returns:**

| Type | Description |
|---|---|
| bool | True if and only if the PDF file exists. |
