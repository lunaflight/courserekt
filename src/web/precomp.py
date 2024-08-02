import itertools
import os
import shutil

from src.web.app import app


def generate_pages() -> None:
    years = ["2122", "2223", "2324", "2425"]
    semesters = ["1", "2"]
    student_types = ["ug", "gd"]

    combinations = itertools.product(years, semesters, student_types)

    try:
        shutil.rmtree("src/web/static/pages")
    except FileNotFoundError:
        pass

    for year, semester, student_type in combinations:
        generate_html(year, semester, student_type)


def generate_html(year: str, semester: str, student_type: str) -> None:
    """
    Generates an HTML file for a specific year, semester, and student type.
    It then saves it in static/pages/{year}/{semester}/{student_type}.

    Args:
    ----
        year: The academic year (e.g., 2223).
        semester: The semester (e.g., 1 or 2).
        student_type: The student type (e.g., "ug" or "gd").
    """
    client = app.test_client()

    data = {
        "year": year,
        "semester": semester,
        "type": student_type,
    }
    response = client.post("/", data=data, follow_redirects=True)

    # Construct the file path
    file_path = f"src/web/static/pages/{year}/{semester}/{student_type}/index.html"

    # Create the necessary directories if they don't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Save the response text as an HTML file
    with open(file_path, "w") as f:
        f.write(response.text)
