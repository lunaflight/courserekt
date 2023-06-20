# NUS Course Registration Analysis

## Purpose

Browsing through Demand Allocation Reports to gain insights about course subscription trends can be a challenging task. It involves parsing multiple PDFs for every round, comparing trends, and examining the classes available. This project aims to streamline this process, making analysis of a course's past popularity more accessible and straightforward.

![Picture of the web app.](https://sussyamongus.s-ul.eu/vqBcKPji)
![Picture of the CLI (Command Line Interface).](https://sussyamongus.s-ul.eu/4uUP55xh)

## Implementation

### CourseReg Records

1. **PDF Storage:** The PDFs are stored in `data/pdfs/[year]/[semester]/[ug/gd]/round_{0,1,2,3}.pdf`.
2. **PDF Parsing:** The PDFs are parsed using [Tabula](https://github.com/tabulapdf/tabula-java) to produce CSV files in `data/raws/[year]/[semester]/[ug/gd]/round_{0,1,2,3}.csv`. Java is used for this purpose, and we use a bash script `./convert_pdfs` to facilitate conversion.
3. **Data Cleaning:** The raw CSV files are passed through `clean_csvs.py` to produce clean CSVs in `data/cleaned/[year]/[semester]/[ug/gd]/round_{0,1,2,3}.csv`.
4. **Database Entry:** The cleaned CSVs are added to the `database.db` by passing them through `csv_to_db.py`.
5. **Web Application:** A Flask-based web application serves the data from the database. It includes a form for users to specify the year, semester, type, and course codes. It returns a neatly formatted table with information about the requested courses.

All of these steps are orchestrated using a Makefile. You just need to add the PDF to the correct folder location, then run `make all`.

### Timetable Planner

The `src/planner` directory contains code that utilizes a backtracking algorithm to plan a non-clashing schedule, given a list of courses, academic year, and semester. The files in this directory include:

1. **Data Fetching**: `nusmods_api.py` queries the NUSMods API based on the provided courses, academic year, and semester, and retrieves a JSON file containing the relevant data.
2. **Scheduler Abstraction**: `Scheduler.py` is a standalone class that handles blocking and unblocking periods of time, checking if any clashes occur. It is used extensively in the timetable backtracking.
3. **Backtracking Finding**: `valid_timetable_finder.py` provides a function that returns a non-clashing timetable schedule, indicating the classes that don't clash with each other.

The use of the backtracking algorithm helps ensure that the generated timetable is valid and free of any schedule clashes. 

Make sure to input the necessary information like your courses, academic year, and semester to retrieve the most accurate and relevant schedule.

### Web App
The `src/web` directory contains code that provides an interface for the above, for a more user-friendly experience.

## Usage

There are two main ways to use this project:

### CourseReg History CLI

<details>
<summary>CLI Usage (Click to Expand)</summary>

To start the CLI, navigate to `src/coursereg_history` and you can use the following command:

```shell
python cli.py

usage: main.py [-h] [-y YEAR] [-s SEMESTER] [-t TYPE] [-c COURSE_CODES [COURSE_CODES ...]] [-p] [-f FILE]
```

Options:
- `-h`, `--help`: Show this help message and exit.
- `-y YEAR`, `--year YEAR`: Read reports from this academic year. This argument is required. Format: (2223 or "22/23" or "22-23" or "2022"). Note: The academic year is based on the starting year.
- `-s SEMESTER`, `--semester SEMESTER`: Read reports from this semester. This argument is required. Format: (1 or 2).
- `-t TYPE`, `--type TYPE`: Read reports from "ug" (undergraduate) or "gd" (graduate). Format: ("ug" or "gd" or "undergraduate" or "graduate").
- `-c COURSE_CODES [COURSE_CODES ...]`, `--course_codes COURSE_CODES [COURSE_CODES ...]`: A list of course codes.
- `-p`, `--percentage`: Converts some unspecified value to a percentage.
- `-f FILE`, `--file FILE`: Read input from a file containing course codes.
- `--no-colour`: Ensures the output has no colour.
- `-v`, `--verbose`: Returns the full API call.

Refer to the examples given below for how to use these arguments.

### Examples

**Query for course data the CLI:**

```shell
python cli.py -y 2223 -t "gd" -s 1 -c "CS4248" "CS5330"
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
python cli.py -y 2223 -s 2 -p -f "example_in.txt"
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

For instance, for the course CS2105 in round 1, 267 students were vying for vacancies per 100 vacancies.
</details>

### Web App

<details>
<summary>Web App Usage (Click to Expand)</summary>

In addition to the CLI, a web app has been created for a more user-friendly experience. The implementation uses Flask with HTML and CSS residing in `templates` and `static` directories respectively.

To start the web app, navigate to `src/web` and you can use the following command:

```shell
python app.py
```

After running the command, open a web browser and navigate to `http://localhost:5000/`. You can then fill the form and press the 'Submit' button to get the analysis.
</details>


## Installation

1. Clone the repository with `git clone https://github.com/et-irl/nus-demand-analysis.git`.
2. Make sure Python and pip are installed on your system. If not, follow the instructions below:

    - **Python and pip:**
        - **Windows/Mac:** Use the installer from [python.org](https://www.python.org/downloads/).
        - **Linux (apt):** `sudo apt-get install python3 python3-pip`
        - **Linux (dnf):** `sudo dnf install python3 python3-pip`
        - **Linux (pacman):** `sudo pacman -S python python-pip`

3. Install the Python dependencies with pip:

    ```shell
    pip install -r requirements.txt
    ```

## Software Engineering Practices

In the development of this project, several software engineering best practices were adopted to ensure code quality, ease of collaboration and maintainability. Below are some of the practices used:

1. **Version Control System (VCS):** The project uses Git as a version control system. It was instrumental in tracking changes and enabling collaboration.

2. **Automated Testing:** Automated testing was performed using Pytest. These tests helped in quickly identifying issues and validating the effectiveness of fixes.

3. ~~**Continuous Integration/Continuous Deployment (CI/CD):**~~ *(Not yet implemented)*

4. **Coding Standards:** The project adheres to common Python coding standards. This includes practices like maintaining less than 80 characters per line, consistent indentation, and the use of descriptive variable names among others. These standards enhance code readability and maintainability.

5. **Design Principles:** The code has been written with simplicity and readability in mind. The functions are kept small and focus on doing one thing well, which is in line with the UNIX philosophy.

6. **Documentation:** Comprehensive documentation was a priority. This README provides an in-depth understanding of the project. The codebase also includes comments where necessary, providing context and explanation for complex code blocks.

7. **Readability and Maintainability:** Type hints and mypy are used extensively in `src/coursereg_history`. This makes sure that errors due to types are avoided before the script is even run, and helps other programmers understand what functions take as input better.

The inclusion of these practices helped ensure the development of a robust and maintainable project while fostering an environment conducive to collaboration.

## Unit Testing

This project employs the built-in `unittest` module in Python for automated testing of the software. It's essential to ensure the robustness of our code and to help catch any potential bugs or problems. 

To run the tests, navigate to the root directory of this project, and run:

```shell
python -m unittest discover
```

This command will search for all the test files in the project and execute them. Any test failures or errors will be reported in the console, making it easy for you to identify and fix the issues.

Unit tests are an essential part of our software development process. They help us maintain the high quality of our code and reduce the likelihood of introducing errors during the development process. By running these tests regularly, you can ensure that any changes or additions you make to the project don't break existing functionality.

## Contributing

Feel free to fork the project, make some changes, and submit a pull request. If you find any bugs or have any suggestions, please open an issue. All contributions are welcomed!
