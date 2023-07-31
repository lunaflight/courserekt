## Project Structure

```
.
├── api.py
    - Contains functions for all queries related to the CourseReg data.
├── clean_csvs.py
    - Python script to convert the raw CSV data to cleaned CSV data.
├── convert_pdfs
    - Bash script to convert the PDFs to raw CSV data using tabula.jar.
├── csv_to_db.py
    - Python script to add cleaned CSV data to database.db.
├── data
    - Contains the PDFs, raw CSVs and cleaned CSVs.
    - All directories are of the form:
    - /{DATA_TYPE}/{YEAR}/{SEMESTER}/{UG or GD}/round_{N}.{DATA_TYPE}
├── database.db
    - Database to store all cleaned CSV data for SQL queries.
├── Makefile
    - Makefile to streamline adding a PDF leading to update the database.
└── tabula.jar
    - JAR file using Tabula to convert PDFs to raw CSV data.
```

## Implementation

### CourseReg Records

It contains code which scrapes and cleans data from the PDFs given by NUS, which is then parsed into easier-to-read formats.

1. **PDF Storage:** The PDFs are stored in `data/pdfs/{YEAR}/{SEMESTER}/{UG or GD}/round_{0,1,2,3}.pdf`.
2. **PDF Parsing:** The PDFs are parsed using [Tabula](https://github.com/tabulapdf/tabula-java) to produce CSV files in `data/raws/{YEAR}/{SEMESTER}/{UG or GD}/round_{0,1,2,3}.csv`. Java is used for this purpose, and we use a bash script `./convert_pdfs` to facilitate conversion.
3. **Data Cleaning:** The raw CSV files are passed through `clean_csvs.py` to produce clean CSVs in `data/cleaned/{YEAR}/{SEMESTER}/{UG or GD}/round_{0,1,2,3}.csv`.
4. **Database Entry:** The cleaned CSVs are added to the `database.db` by passing them through `csv_to_db.py`.
5. **API:** Queries about the courses can be made through the `api.py` file, which executes the relevant SQL queries to retrieve the data.

All of these steps are orchestrated using a Makefile.

## Usage

### `api.py`

#### get_all_data

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

#### get_data

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

**Parameters:**

| Name | Type | Description | Default |
|---|---|---|---|
| year | Union[str, int] | The academic year. | None |
| semester | Union[str, int] | The semester. | None |
| ug_gd | str | The undergraduate/graduate indicator. | None |
| code | str | The course code. | None |
| conn | Optional[sqlite3.Connection] | Optional database connection object. | None |

**Returns:**

| Type | Description |
|---|---|
| CourseData | The course data. |
