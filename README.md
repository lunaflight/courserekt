# NUS Course Registration Analysis

## Purpose

Browsing through Demand Allocation Reports to gain insights about course subscription trends can be a challenging task. It involves parsing multiple PDFs for every round, comparing trends, and examining the classes available. This project aims to streamline this process, making analysis of a course's past popularity more accessible and straightforward.

## Implementation

This project follows these steps:

1. **PDF Storage:** The PDFs are stored in `data/pdfs/[year]/[semester]/[ug/gd]/round_{0,1,2,3}.pdf`.
2. **PDF Parsing:** The PDFs are parsed using [Tabula](https://github.com/tabulapdf/tabula-java) to produce CSV files in `data/raws/[year]/[semester]/[ug/gd]/round_{0,1,2,3}.csv`. Java is used for this purpose, and we use a bash script `./convert_pdfs` to facilitate conversion.
3. **Data Cleaning:** The raw CSV files are passed through `clean_csvs.py` to produce clean CSVs in `data/cleaned/[year]/[semester]/[ug/gd]/round_{0,1,2,3}.csv`.
4. **Database Entry:** The cleaned CSVs are added to the `database.db` by passing them through `csv_to_db.py`.

All of these steps are orchestrated using a Makefile. You just need to add the PDF to the correct folder location.

## Usage

The script accepts several command-line arguments:

```shell
usage: main.py [-h] [-y YEAR] [-s SEMESTER] [-t TYPE] [-c COURSE_CODES [COURSE_CODES ...]] [-p] [-f FILE]
```

Options:
- `-h`, `--help`: Show the help message and exit.
- `-y YEAR`, `--year YEAR`: Read reports from this year.
- `-s SEMESTER`, `--semester SEMESTER`: Read reports from this semester.
- `-t TYPE`, `--type TYPE`: Read reports from "ug" or "gd".
- `-c COURSE_CODES [COURSE_CODES ...]`, `--course_codes COURSE_CODES [COURSE_CODES ...]`: A list of course codes to fetch data for.
- `-p`, `--percentage`: Change the output format to a percentage of subscription relative to vacancies.
- `-f FILE`, `--file FILE`: Read input from a file containing a list of course codes. The course codes in the file should be separated by new lines.

### Examples

**Query for course data for specific courses:**

```shell
python main.py -y 2223 -t "gd" -s 1 -c "CS4248" "CS5330"
```
This command fetches information for the courses "CS4248" and "CS5330" for the year 22/23, semester 1, as a graduate student. 

The output would look like this:

```shell
CS4248
L1: 28 / 5  -> N/A     -> N/A     -> 3 / 0  
L2: 76 / 65 -> 7 / 16  -> 6 / 15  -> 12 / 13
CS5330
L1: 21 / 35 -> 9 / 26  -> 2 / 17  -> N/A
```
Here, each line shows the demand and vacancies for a particular course. The entries follow the format `demand / vacancies` and the arrows indicate the progression from round 0 to 3. `N/A` indicates that data for that particular round was not found. 

For instance, for the course CS4248 in round 0, there were 28 students registered for the course, but only 5 vacancies available. By round 3, only 3 students were registered, and there were no vacancies left. 

### Example

```shell
python main.py -y 2223 -s 2 -p -f "example_in.txt"
```
This command fetches information for the courses listed in `example_in.txt` (separated by new lines) for the year 22/23, semester 2, as an undergraduate. The `-p` flag indicates that the output will display percentage of subscription relative to vacancies.

The output would look like this:

```markdown
CS2101 NOT FOUND
CS2102
L1: 182.0 -> 192.0 -> 210.0 -> 88.0 
L2: N/A   -> 217.0 -> 220.0 -> 100.0
CS2103
L1: 80.0 -> 65.0 -> 43.0 -> 71.0
CS2104 NOT FOUND
CS2105
L1: 128.0 -> 267.0 -> 300.0 -> 300.0
L2: N/A   -> 212.0 -> 100.0 -> 300.0
CS2106
L1: 155.0  -> 80.0   -> 150.0  -> 1100.0
L2: N/A    -> 115.0  -> 183.0  -> 900.0 
CS2107
L1: 144.0 -> 105.0 -> 25.0  -> NaN  
L2: N/A   -> 18.0  -> 5.0   -> 29.0 
CS2108
L1: 49.0 -> 26.0 -> 15.0 -> 31.0
CS2109 NOT FOUND
```
Here, the output consists of the course code followed by the round-wise status of that course. The arrows represent the progression from round 0 to 3. Each number represents the status of that course in that round. If a course isn't found in the data, a "NOT FOUND" message is displayed. A NaN is displayed if 0 vacancies were available.

For instance, for the course CS2105 in round 1, there were 267 students vying per 100 vacancies.


## Installation

1. Clone the repository with `git clone https://github.com/et-irl/nus-demand-analysis.git`.
2. Make sure Java, Python, and pip are installed on your system. If not, follow the instructions below:

    - **Java:** [Windows/Mac/Linux](https://www.java.com/en/download/help/download_options.html)
    - **Python and pip:**
        - **Windows/Mac:** Use the installer from [python.org](https://www.python.org/downloads/).
        - **Linux (apt):** `sudo apt-get install python3 python3-pip`
        - **Linux (dnf):** `sudo dnf install python3 python3-pip`
        - **Linux (pacman):** `sudo pacman -S python python-pip`

3. Install the Python dependencies with pip:

    ```shell
    pip install -r requirements.txt
    ```

## Contributing

Feel free to fork the project, make some changes, and submit a pull request. If you find any bugs or have any suggestions, please open an issue. All contributions are welcomed!
