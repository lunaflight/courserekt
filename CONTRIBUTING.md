## Project Structure

```
.
├── .github/workflows
    - Contains the files for continuous integration.
├── .gitignore
    - Contains the list of files to ignore upon committing to git.
├── README.md
    - Documentation
├── docs/images
    - Contains all assets for the documentation of the project.
├── requirements.txt
    - Contains the Python dependencies required in the project.
├── src
    - Contains all source code for the project.
├── tests
    - Contains all code used for testing the project.
├── .vercelignore
    - Contains the list of files to ignore upon Vercel deployment.
└── vercel.json
    - Contains the configuration for Vercel deployment.
```

Read the corresponding `README.md` files in the respective subdirectories for more information.

## For Devs:

### Installation

1. Clone the repository with `git clone https://github.com/et-irl/courserekt.git`.
2. Navigate to `src/history` and run `make all`. (This will generate `database.db`.)
3. Make sure Python and pip are installed on your system. If not, follow the instructions below:
    - **Python and pip:**
        - **Windows/Mac:** Download the installer from the [Python website](https://www.python.org/downloads/).
        - **Linux (apt):** `sudo apt-get install python3 python3-pip`
        - **Linux (dnf):** `sudo dnf install python3 python3-pip`
        - **Linux (pacman):** `sudo pacman -S python python-pip`
4. Navigate to the **project root** and set up a virtual environment with `python -m venv venv`.
    - A virtual environment ensures that everyone is working with the same set of dependencies.
5. Activate the virual environment:
    - Activating:
        - **Windows:** `venv\Scripts\activate`
        - **Mac/Linux:** `source venv/bin/activate`
    - You should see the `(venv)` prefix in your command prompt.
6. Install the Python dependencies with pip:
    ```shell
    pip install -r requirements.txt
    ```
7. When you are done, you can deactivate the virtual environment with `deactivate`.

### Web App

To start the web app, navigate to the **project root** and do the following:

```shell
python -m src.web.main
```

This will cache all pages.
Optionally, you may supply the following to `python -m src.web.main`.
- `-p`, `--port PORT`: Port where the app is run. Otherwise, it defaults to `5000`.
- `-s`, `--skip-precompute`: Use the existing files in `static/pages` to load the HTML instead.

After running the command, open a web browser and navigate to `http://localhost:5000/`. 

### Unit Testing

This project employs the built-in `unittest` module in Python for automated testing.

To run the tests, navigate to the **project root** of this project, and run:

```shell
python -m unittest discover
```

### Static Code Analysis

First, ensure Mypy is installed. If it is not, run `pip install mypy`.

To run the analysis, navigate to the **project root** of this project, and run:

```shell
mypy .
```

### Adding New CourseReg Data
When new data is released, the program can be updated easily. You can follow the following steps to update it.

1. Ensure Java is installed. This is required to run [Tabula](https://github.com/tabulapdf/tabula-java).
    - **Windows/Mac:** Download the installer from the [Oracle website](https://www.oracle.com/java/technologies/javase-jdk11-downloads.html).
    - **Linux (apt):** `sudo apt install default-jdk`
    - **Linux (dnf):** `sudo dnf install java-latest-openjdk`
    - **Linux (pacman):** `sudo pacman -S jdk-openjdk`
2. Navigate to `src/history/coursereg_history/data/pdfs`. 
3. Create the relevant directory by running `mkdir -p YEAR/SEM/TYPE`. For example, `2324/1/ug` or `2425/2/gd`.
4. Add the "Course Class Demand and Allocation Report" PDF in the relevant directory, naming it `round_N.pdf`.
For example, `round_0.pdf`.
5. Navigate to `src/history/vacancy_history/data/pdfs`. 
6. Create the relevant directory by running `mkdir -p YEAR/SEM`. For example, `2324/1` or `2425/2`.
7. Add the "Course Class Vacancy Report" PDF in the relevant directory, naming it `round_N.pdf`.
8. Navigate to `src/history`. Run `make all`.
9. You're done! The data should have been added successfully and ready to use.

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
5. Deploy your application to Vercel: `vercel`.

This will initiate the deployment process, and Vercel will guide you through the necessary steps to deploy your application.
