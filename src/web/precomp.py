from src.web.app import app
import itertools
import os


def main():
    # List of years
    years = ["2122", "2223", "2324"]

    # List of semesters
    semesters = ["1", "2"]

    # List of student types
    student_types = ["ug", "gd"]

    # Generate all combinations
    combinations = itertools.product(years, semesters, student_types)

    for year, semester, student_type in combinations:
        generate_html(year, semester, student_type)


def generate_html(year: str, semester: str, student_type: str):
    client = app.test_client()
    client.testing = True

    data = {
        'year': year,
        'semester': semester,
        'type': student_type
    }
    response = client.post('/', data=data, follow_redirects=True)

    # Extract the year, semester, and type from the request data
    year, semester, type = data['year'], data['semester'], data['type']

    # Construct the file path
    file_path = f"src/web/static/pages/{year}/{semester}/{type}/index.html"

    # Create the necessary directories if they don't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Save the response text as an HTML file
    with open(file_path, "w") as f:
        f.write(response.text)

    print(f"Saved HTML content to: {file_path}")


if __name__ == '__main__':
    main()
