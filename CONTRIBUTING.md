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
- The project assumes no setup of virtual environments. If you know how to
  manage your own virtual environment, then remove the activation and
  deactivation of the venv of scripts in `scripts/`.

### Installation

Initial cloning of the project:
```sh
git clone https://github.com/lunaflight/courserekt.git &&
cd courserekt &&
chmod -R +x scripts/
```

**Important:** Replace the link for `git clone` with the link of your repository, if you have forked it.

Building the project (only run this once):
```sh
./scripts/init.sh
```

**Please be patient. This might take some time (around 2 minutes, on my machine).**

Note that this utilises [tabula-py](https://pypi.org/project/tabula-py/), a thin Python wrapper around [tabula-java](https://github.com/tabulapdf/tabula-java), a Java library for extracting tables from PDF files. You may find yourself needing to install Java:
    - **ArchLinux:** `sudo pacman -S jre-openjdk-headless` should suffice. [Variants found here.](https://wiki.archlinux.org/title/java)
    - **Fedora Linux:** Please refer to [your distribution's installation instructions](https://docs.fedoraproject.org/en-US/quick-docs/installing-java/). Choose an appropriate minimal (or more) JRE to install.

### Virtual Environment & Dependencies
A virtual environment ensures that everyone is working with the same set of dependencies.

The dependencies described in `local-requirements.txt` describe all the dependencies used in the development of the project.

- This includes:
    - Building the database
    - Linting
    - Type checking
    - Deploying the web app

`requirements.txt`, on the other hand, is used for deployment on Vercel, which only allows 250MB of libraries to be imported. Hence, we keep the number of libraries to a minimum in `requirements.txt`.

### Branches
- `main` refers to the branch being deployed on Vercel which supports only Python 3.9 syntax.
- `py312-github-pages` refers to the branch that employs Python 3.12 syntax in preparation to move to GitHub Pages.

### Web App

To start the web app, run the following:
```sh
./scripts/main.sh
```

This will take some time as it precomputes and caches all pages.

You may instead run the underlying command directly. 
```sh
python -m src.web.main --help
```

### Sanity Checks

Run the following to ensure run unit testing, static code analysis and the style checker.
```sh
./scripts/checks.sh
```

This uses `unittest`, `mypy` and `ruff`.

### Adding New CourseReg Data
Vacancy and CourseReg data should be added at the same time.

Run the following:
```sh
./scripts/add_pdf_data.sh ACAD_YEAR SEMESTER ROUND
```

For example, to only compute PDFs in the year `22/23`
and the semester `1`, during round `0`, you should run
`./scripts/add_pdf_data.sh 2223 1 0`.

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
