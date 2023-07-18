# :rocket: Check out the web app!
## [Coursereg Scraper](https://coursereg-scraper.vercel.app/history) :computer:

Click the link above to explore the interactive web app!

## Purpose

Browsing through Demand Allocation Reports to gain insights about course subscription trends can be a challenging task. It involves looking at multiple PDFs for every round, comparing trends, and examining the classes available. This project aims to streamline this process, making analysis of a course's past popularity more accessible and straightforward.

Well, at least that was the humble starting idea, but let's see how much further we can go! :p

![Picture of the web app.](https://sussyamongus.s-ul.eu/vqBcKPji)
![Picture of the CLI (Command Line Interface).](https://sussyamongus.s-ul.eu/4uUP55xh)
![Picture of the scheduler output.](https://sussyamongus.s-ul.eu/crmrfNNo)

## Implementation

### CourseReg Records

The files for this reside in `src/coursereg_history`.

It contains code which scrapes and cleans data from the PDFs given by NUS, which is then parsed into easier-to-read formats.

1. **PDF Storage:** The PDFs are stored in `data/pdfs/[year]/[semester]/[ug/gd]/round_{0,1,2,3}.pdf`.
2. **PDF Parsing:** The PDFs are parsed using [Tabula](https://github.com/tabulapdf/tabula-java) to produce CSV files in `data/raws/[year]/[semester]/[ug/gd]/round_{0,1,2,3}.csv`. Java is used for this purpose, and we use a bash script `./convert_pdfs` to facilitate conversion.
3. **Data Cleaning:** The raw CSV files are passed through `clean_csvs.py` to produce clean CSVs in `data/cleaned/[year]/[semester]/[ug/gd]/round_{0,1,2,3}.csv`.
4. **Database Entry:** The cleaned CSVs are added to the `database.db` by passing them through `csv_to_db.py`.
5. **Web Application:** A Flask-based web application serves the data from the database. It includes a form for users to specify the year, semester, type, and course codes. It returns a neatly formatted table with information about the requested courses.

All of these steps are orchestrated using a Makefile.

### Timetable Planner

The files for this reside in `src/planner`.

It contains code that utilizes a backtracking algorithm to plan a non-clashing schedule, given a list of courses, academic year, and semester. The files in this directory include:

1. **Data Fetching**: `nusmods_api.py` queries the NUSMods API based on the provided courses, academic year, and semester, and retrieves a JSON file containing the relevant data.
2. **Scheduler Abstraction**: `Scheduler.py` is a standalone class that handles blocking and unblocking periods of time, checking if any clashes occur. It is used extensively in the timetable backtracking.
3. **Backtracking Finding**: `valid_timetable_finder.py` provides a function that returns a non-clashing timetable schedule, indicating the classes that don't clash with each other.
4. **URL Generating**: `url_generator.py` provides the relevant NUSMods link upon finding a valid timetable, allowing you to import the data easily.

The use of the backtracking algorithm helps ensure that the generated timetable is valid and free of any schedule clashes. 

Make sure to input the necessary information like your courses, academic year, and semester to retrieve the most accurate and relevant schedule.

### Web App
The `src/web` directory contains code that provides an interface for the above, for a more user-friendly experience.

## Usage

There are a few main ways to use this project:

### CourseReg History CLI

<!-- <details> -->
<!-- <summary>CLI Usage (Click to Expand)</summary> -->

To start the CLI, navigate to the **project root** and you can use the following command:

```shell
python -m src.coursereg_history.cli

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
python -m src.coursereg_history.cli -y 2223 -t "gd" -s 2 -c "CS4248" "CS5330"
```
This command fetches information for the courses "CS4248" and "CS5330" for the year 22/23, semester 1, as a graduate student. 

The output could look like this:

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
python -m src.coursereg_history.cli -y 2223 -s 2 -p -f "example_in.txt"
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
<!-- </details> -->

### Timetable Planner CLI

<!-- <details> -->
<!-- <summary>CLI Usage (Click to Expand)</summary> -->

To start the CLI, navigate to the **project root** and you can use the following command:

```shell
python -m src.planner.cli -h

usage: cli.py [-h] [-y YEAR] -s SEMESTER -c COURSES [COURSES ...]
              [-w WHITELIST [WHITELIST ...]]
```

Options:
- `-h`, `--help`: Show this help message and exit.
- `-y YEAR`, `--year YEAR`: Specify the academic year. This argument accepts the following formats: "2022-2023", "22-23", "22/23", "2223".
- `-s SEMESTER`, `--semester SEMESTER`: The semester number (1 or 2).
- `-c COURSES [COURSES ...]`, `--courses COURSES [COURSES ...]`: Specify the course codes. For example, `-c "LAJ2201" "CS2100"`.
- `-w WHITELIST [WHITELIST ...]`, `--whitelist WHITELIST [WHITELIST ...]`: Specify the whitelist as a series of "COURSE:TYPE" strings. For example, `-w "CS2100:LEC,TUT" "LAJ2201:LEC"`.

Refer to the examples given below for how to use these arguments.

### Examples

```shell
python -m src.planner.cli -s 1 -c "CS2100" "CS2102" "CS2103T" "CS2105" "CS2106" "CS2107" "CS2109S" -w "CS2100:REC"
```
This command tries to find a valid timetable arrangement with no clashes for the courses listed. This will be for the default (current) year, semester 1. The `-w` flag indicates the Recitation (REC) slot will be treated as not taking up time. This can be used to manually resolve conflicts.

The output would look like this:

```markdown
https://nusmods.com/timetable/sem-1/share?CS2100=LAB:11,TUT:03,LEC:1,REC:1&CS2109S=TUT:09,LEC:1&CS2103T=LEC:G01&CS2102=TUT:16,LEC:1&CS2105=TUT:03,LEC:1V&CS2106=TUT:06,LAB:01,LEC:1&CS2107=TUT:11,LEC:1
```

A link will be returned in the command line, allowing you to straightforwardly import it into NUSMods.

<!-- </details> -->

### Web App

<!-- <details> -->
<!-- <summary>Web App Usage (Click to Expand)</summary> -->

The files for this reside in `src/web`.

In addition to the CLI, a web app has been created for a more user-friendly experience. The implementation uses Flask with HTML and CSS residing in `templates` and `static` directories respectively.

To start the web app, navigate to the **project root** and you can use the following command:

```shell
python -m src.web.app 
```

Options:
- `-h`, `--help`: Show this help message and exit
- `--port PORT`: Port where the app is run.

After running the command, open a web browser and navigate to `http://localhost:5000/`. 

This will lead you to a self-explanatory website that provides a more user-friendly interface for the command line interface.
<!-- </details> -->


## Installation

1. Clone the repository with `git clone https://github.com/et-irl/nus-tools.git`.
2. Make sure Python and pip are installed on your system. If not, follow the instructions below:

    - **Python and pip:**
        - **Windows/Mac:** Use the installer from [python.org](https://www.python.org/downloads/).
        - **Linux (apt):** `sudo apt-get install python3 python3-pip`
        - **Linux (dnf):** `sudo dnf install python3 python3-pip`
        - **Linux (pacman):** `sudo pacman -S python python-pip`

3. Navigate to the **project root** and install the Python dependencies with pip:

    ```shell
    pip install -r requirements.txt
    ```

## For Devs:

### Unit Testing

This project employs the built-in `unittest` module in Python for automated testing of the software. It's essential to ensure the robustness of our code and to help catch any potential bugs or problems. 

To run the tests, navigate to the **project root** of this project, and run:

```shell
python -m unittest discover
```

This command will search for all the test files in the project and execute them. Any test failures or errors will be reported in the console, making it easy for you to identify and fix the issues.
Unit tests are an essential part of our software development process. They help us maintain the high quality of our code and reduce the likelihood of introducing errors during the development process. By running these tests regularly, you can ensure that any changes or additions you make to the project don't break existing functionality.

### Adding of new CourseReg data
When new data is released, the program can be updated easily. You can follow the following steps to update it.
1. Ensure Java is installed. This is required to run [Tabula](https://github.com/tabulapdf/tabula-java).
    - **Windows/Mac:** Download the installer from the [Oracle website](https://www.oracle.com/java/technologies/javase-jdk11-downloads.html).
    - **Linux (apt):** `sudo apt install default-jdk`
    - **Linux (dnf):** `sudo dnf install java-latest-openjdk`
    - **Linux (pacman):** `sudo pacman -S jdk-openjdk`
2. Navigate to `src/coursereg_history/data/pdfs`. 
3. Create the relevant directory by running `mkdir -p YEAR/SEM/TYPE`. For example, `2324/1/ug` or `2425/2/gd`.
4. Add the pdf in the relevant directory, naming it `round_N.pdf`. For example, `round_0.pdf`.
5. Navigate to `src/coursereg_history`. Run `make all`.
6. You're done! The data should have been added successfully and ready to use.

### Deployment to Vercel

To deploy your application to Vercel, follow these steps:

1. Ensure npm is installed. This is required to manage dependencies and execute commands.
    - **Windows/Mac:** Download the Node.js installer from the [Node.js website](https://nodejs.org/en/download/).
        - **Linux (apt)** `sudo apt install nodejs npm`
        - **Linux (dnf)** `sudo dnf install nodejs npm`
        - **Linux (pacman)** `sudo pacman -S nodejs npm`
2. Install the Vercel CLI globally: `npm install -g vercel`.
3. Log in to Vercel by running the following command: `vercel login`.
4. Navigate to the project root in the terminal.
5. Deploy your application to Vercel: `vercel --prod`.

This will initiate the deployment process, and Vercel will guide you through the necessary steps to deploy your application.

## Contributing

Feel free to fork the project, make some changes, and submit a pull request. If you find any bugs or have any suggestions, please open an issue. All contributions are welcomed!
