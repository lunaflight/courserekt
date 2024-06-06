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
- `src/history`: [Dealing with and querying PDF data](src/history/README.md)
- `src/web`: [Generating and serving web pages](src/web/README.md)

## For Devs:

### About

- The project uses Python 3.9 syntax. (See `Branches` for more information.)

### Installation

```sh
git clone https://github.com/lunaflight/courserekt.git &&
cd courserekt &&
python -m venv venv &&
echo "export PYTHONPATH=\$(pwd)" >> venv/bin/activate &&
source venv/bin/activate &&
pip install -r local-requirements.txt &&
python -m src.history.build
```

**Important:** Replace the link for `git clone` with the link of your repository, if you have forked it.

**Please be patient. This might take some time (around 2 minutes, on my machine).**

**An explanation:**
1. First, we clone the repository from GitHub.

2. Then, we set up a virtual environment with `python -m venv venv`, as a good practice when working with libraries and projects.

3. We set up `PYTHONPATH` upon activating the virtual environment, to fix issues of being unable to find `src`.
    - Upon activating `venv` every time in the future, `PYTHONPATH` will be set up.

4. We install all the required dependencies as outlined in `local-requirements.txt`, to ensure everybody works with the same dependencies.
    - You may run into issues during `pip install` if you do not have the latest version of python.
    - You may just continue from this command (and not run all commands from `git clone`) if it fails.

5. We run `python -m src.history.build` to generate `database.db`.
    - Note that this utilises [tabula-py](https://pypi.org/project/tabula-py/), a thin Python wrapper around [tabula-java](https://github.com/tabulapdf/tabula-java), a Java library for extracting tables from PDF files. You may find yourself needing to install Java:
        - **ArchLinux:** `sudo pacman -S jre-openjdk-headless` should suffice. [Variants found here.](https://wiki.archlinux.org/title/java)
        - **Fedora Linux:** Please refer to [your distribution's installation instructions](https://docs.fedoraproject.org/en-US/quick-docs/installing-java/). Choose an appropriate minimal (or more) JRE to install.

Note: If at any point, one of these commands fail (such as being unable to install the dependencies), you may have to rectify that command first, before continuing with the rest of the installation script.

### Virtual Environment
A virtual environment ensures that everyone is working with the same set of dependencies.

The dependencies described in `local-requirements.txt` describe all the dependencies used in the development of the project.

- This includes:
    - Building the database
    - Linting
    - Type checking
    - Deploying the web app

`requirements.txt`, on the other hand, is used for deployment on Vercel, which only allows 250MB of libraries to be imported. Hence, we keep the number of libraries to a minimum in `requirements.txt`.

**Activate the virtual environment:**
- Activating:
    - **Windows:** `venv\Scripts\activate`
    - **Mac/Linux:** `source venv/bin/activate`
- You should see the `(venv)` prefix in your command prompt.

**Deactivate the virtual environment:**
- `deactivate`
- You should see the `(venv)` prefix disappear in your command prompt.

### Branches
- `main` refers to the branch being deployed on Vercel which supports only Python 3.9 syntax.
- `py312-github-pages` refers to the branch that employs Python 3.12 syntax in preparation to move to GitHub Pages.

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
python -m unittest
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
