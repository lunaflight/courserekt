# :rocket: CourseRekt
## [Visit the website here!](https://courserekt.vercel.app/) :computer:

![Image of the website](https://i.imgur.com/uDUFnKh.png)

## Purpose

It is rather unfortunate that NUS does not keep a record of the Demand Allocation Reports. Furthermore, the data is presented in such a verbose and hard-to-visualise way. This app aims to streamline this process, making analysis of a course's past popularity more accessible and straightforward.

## For Users:

### Search Bar

You can delimit your search with spaces. For example, "AC5001 CS2" will show all course codes that have "AC5001" or "CS2" in its name.

### Accessing the PDF data

You can click the column headers to access the raw PDF data used to generate the table for the respective year, semester, and undergraduate/graduate type.

### Interpreting table cells

Each cell corresponds to the data in the PDF for the course's class and round number, in the format `x / y`, where `x` is the `Demand` and y is the `Vacancy` as per the PDF.

- If `y` is displayed as `∞`, the `Vacancy` in the PDF is `-`.
- If `N/A` is displayed, then the class data was not found in this PDF.

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

### Web App
The `src/web` directory contains code that provides an interface for the above, for a more user-friendly experience.

## For Devs:

### Installation

1. Clone the repository with `git clone https://github.com/et-irl/nus-tools.git`.
2. Make sure Python and pip are installed on your system. If not, follow the instructions below:
    - **Python and pip:**
        - **Windows/Mac:** Download the installer from the [Python website](https://www.python.org/downloads/).
        - **Linux (apt):** `sudo apt-get install python3 python3-pip`
        - **Linux (dnf):** `sudo dnf install python3 python3-pip`
        - **Linux (pacman):** `sudo pacman -S python python-pip`
3. Navigate to the **project root** and install the Python dependencies with pip:
    ```shell
    pip install -r requirements.txt
    ```

### Web App

To start the web app, navigate to the **project root** and you can use the following command:

```shell
python -m src.web.app 
```

Options:
- `-h`, `--help`: Show this help message and exit
- `--port PORT`: Port where the app is run.

After running the command, open a web browser and navigate to `http://localhost:5000/`. 

### Unit Testing

This project employs the built-in `unittest` module in Python for automated testing.

To run the tests, navigate to the **project root** of this project, and run:

```shell
python -m unittest discover
```

### Adding New CourseReg Data
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
