import os
from argparse import ArgumentParser
from typing import Any

from flask import Flask, Response, render_template, request, send_from_directory

from src.history.api import INF, get_all_data, get_pdf_filepath, pdf_exists, get_latest_year_and_sem_with_data

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@app.context_processor
def context_processor() -> dict[Any, Any]:
    """
    Context processor function for the Flask app.

    This function provides additional variables to be
    automatically available in all Jinja templates
    rendered by the Flask app.
    """
    return {"INF":INF, "pdf_exists":pdf_exists}


@app.route("/", methods=["GET", "POST"])
def history() -> str:
    """
    Display course history based on the selected
    academic year, semester, and course type.

    Returns
    -------
        str: The rendered HTML content to display the course history.
    """
    # Adjust the default parameters as necessary.
    (latestYear, latestSem) = get_latest_year_and_sem_with_data()
    year = request.form.get("year", latestYear)
    semester = request.form.get("semester", latestSem)
    student_type = request.form.get("type", "ug")

    # Check if the precomputed HTML file exists
    filepath = os.path.join(BASE_DIR, "static/pages", year, semester, student_type, "index.html")
    if os.path.exists(filepath):
        # Serve the precomputed HTML
        with open(filepath, "r") as f:
            return f.read()

    # Fallback to dynamic rendering if the file doesn't exist
    output, error = [], None
    try:
        output = get_all_data(year, semester, student_type)
    except ValueError as e:
        error = e

    return render_template("history.html", output=output, error=error)


def _serve_file(filepath: str) -> Response:
    """
    Helper function which serves the file based on the filepath.
    This is because the Flask `send_from_directory` function does
    not accept a single absolute filepath.

    Parameters
    ----------
        filepath (str): The absolute filepath to serve.

    Returns
    -------
        Response: The file to be served.
    """
    directory, filename = os.path.split(filepath)
    return send_from_directory(directory, filename)


@app.route("/pdfs/<int:year>/<int:semester>/<string:student_type>/"
           "round_<int:round_num>.pdf")
def serve_pdf(
        year: str | int,
        semester: str | int,
        student_type: str,
        round_num: str | int) -> Response:
    """
    Serve a PDF file from the specified directory.
    It will be hosted in the directory:
        `/pdfs/year/semester/student_type/round_number.pdf`.

    Parameters
    ----------
        year (int): The year of the PDF file.
        semester (int): The semester of the PDF file.
        student_type (str): The student type of the PDF file.
        round_num (int): The round number of the PDF file.

    Returns
    -------
        Response: The PDF file to be served.
    """
    return _serve_file(str(get_pdf_filepath(year, semester, student_type, round_num)))


def main() -> None:
    parser = ArgumentParser(description="Web app for CourseRekt")
    parser.add_argument("--port", type=int, nargs=1, default=5000,
                        help="Port where the app is run.")
    args = parser.parse_args()

    app.run(host="0.0.0.0", port=args.port, debug=True)


if __name__ == "__main__":
    main()
