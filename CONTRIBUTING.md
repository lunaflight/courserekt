## Project Structure

```
.
├── .github/workflows
    - Contains the files for continuous integration.
├── .gitignore
    - Contains the list of files to ignore upon committing to git.
├── CONTRIBUTING.md
    - Documentation for developers
├── docs/images
    - Contains all assets for the documentation of the project.
├── README.md
    - Documentation for users
├── local-requirements.txt
    - Contains all the Python dependencies required in the project.
├── requirements.txt
    - Contains only the Python dependencies required to deploy the project on vercel.
├── ruff.toml
    - Contains the Ruff configuration specified for the project.
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

1. Clone the repository with `git clone https://github.com/lunaflight/courserekt.git`.
2. Using a Virtual Environment (as outlined below), or otherwise, install all python dependencies of the project.
3. From the **project root**, run the following to set up `PYTHONPATH`. This will resolve issues of scripts being unable to find `src` as a module.
```sh
export PYTHONPATH=$(pwd);
```
4. From the **project root**, run `python -m src.history.build`. (This will generate `database.db`.)

### Setting up a Virtual Environment
A virtual environment ensures that everyone is working with the same set of dependencies.

The dependencies described in `local-requirements.txt` describe all the dependencies used in the development of the project.

- This includes:
    - Building the database
    - Linting
    - Type checking
    - Deploying the web app

`requirements.txt`, on the other hand, is used for deployment on Vercel, which only allows 250MB of libraries to be imported. Hence, we keep it to a minimum in `requirements.txt`.

1. Navigate to the **project root** and set up a virtual environment with `python -m venv venv`.
2. Activate the virual environment:
    - Activating:
        - **Windows:** `venv\Scripts\activate`
        - **Mac/Linux:** `source venv/bin/activate`
    - You should see the `(venv)` prefix in your command prompt.
3. Install the Python dependencies with pip:
    ```shell
    pip install -r local-requirements.txt
    ```
4. When you are done, you can deactivate the virtual environment with `deactivate`.

### Web App

To start the web app, navigate to the **project root** and do the following:

```shell
python -m src.web.main
```

This will precompute and cache all pages.
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

First, ensure Mypy is installed. If it is not, run `pip install mypy` or `python -m pip install mypy`.

To run the analysis, navigate to the **project root** of this project, and run:

```shell
python -m mypy --strict .
```

### Style Checker

First, ensure Ruff is installed. If it is not, run `pip install ruff` or `python -m pip install ruff`.

To run the checker, navigate to the **project root** of this project, and run:

```shell
python -m ruff check
```

### Adding New CourseReg Data
When new data is released, the program can be updated easily. You can follow the following steps to update it.

**Important:** Vacancy and CourseReg data should be added at the same time. This is due to how `merge.py` works at the moment - we depend on both data existing. For example, Vacancy data should not be added without its CourseReg data counterpart.

1. Navigate to `src/history/coursereg_history/data/pdfs`. 
2. Create the relevant directory by running `mkdir -p YEAR/SEM/TYPE`. For example, `2324/1/ug` or `2425/2/gd`.
3. Add the "Course Class Demand and Allocation Report" PDF in the relevant directory, naming it `round_N.pdf`.
For example, `round_0.pdf`.
4. Navigate to `src/history/vacancy_history/data/pdfs`. 
5. Create the relevant directory by running `mkdir -p YEAR/SEM`. For example, `2324/1` or `2425/2`.
6. Add the "Course Class Vacancy Report" PDF in the relevant directory, naming it `round_N.pdf`.
7. Navigate to the **project root**. Run `python -m src.history.build`.
    - This command forces a recomputation of all known PDFs in the project.

    - **Please be patient. This might take some time (around 2 minutes, on my machine).**

    - To only compute the newly added PDFs, you may use additional flags. Run it with `--help` for more information.

    - For example, to only compute PDFs in the year `22/23` and the semester `1`, during round `0`:
    ```shell
    python -m src.history.build -y 2223 -s 1 -r 0
    ```
8. You're done! The data should have been added successfully and ready to use.

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
