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

## Project Structure

```
.
├── .github/workflows
    - Contains the files for continuous integration.
├── .gitignore
    - Contains the list of files to ignore upon committing to git.
├── README.md
    - Documentation
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
2. Make sure Python and pip are installed on your system. If not, follow the instructions below:
    - **Python and pip:**
        - **Windows/Mac:** Download the installer from the [Python website](https://www.python.org/downloads/).
        - **Linux (apt):** `sudo apt-get install python3 python3-pip`
        - **Linux (dnf):** `sudo dnf install python3 python3-pip`
        - **Linux (pacman):** `sudo pacman -S python python-pip`
3. Navigate to the **project root** and set up a virtual environment with `python -m venv venv`.
    - A virtual environment ensures that everyone is working with the same set of dependencies.
4. Activate the virual environment:
    - Activating:
        - **Windows:** `venv\Scripts\activate`
        - **Mac/Linux:** `source venv/bin/activate`
    - You should see the `(venv)` prefix in your command prompt.
5. Install the Python dependencies with pip:
    ```shell
    pip install -r requirements.txt
    ```
6. When you are done, you can deactivate the virtual environment with `deactivate`.

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
5. Deploy your application to Vercel: `vercel`.

This will initiate the deployment process, and Vercel will guide you through the necessary steps to deploy your application.

## Contributing

Feel free to fork the project, make some changes, and submit a pull request. If you find any bugs or have any suggestions, please open an issue. All contributions are welcomed!

## Contributors

Thank you to all of our contributors!

<a href="https://github.com/et-irl/courserekt/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=et-irl/courserekt" />
</a>

Made with [contrib.rocks](https://contrib.rocks).
