import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from flask import Flask, render_template, request
from coursereg_history.api import get_data
from planner.cli import parse_and_generate_url

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        year = request.form.get('year')
        semester = request.form.get('semester')
        type = request.form.get('type')
        course_codes = request.form.get('course_codes').split()

        output = []
        errors = []
        for course_code in course_codes:
            data = get_data(year, semester, type, course_code)
            if data["error"] is None:
                output.append(data)
            else:
                errors.append(data["error"])

        return render_template('index.html', output=output, errors=errors)
    else:
        return render_template('index.html')


@app.route('/scheduler', methods=['GET', 'POST'])
def scheduler():
    if request.method == 'POST':
        year = request.form.get('year')
        semester = request.form.get('semester')
        course_codes = request.form.get('course_codes').split()
        whitelist = request.form.get('whitelist').split()

        # Run your scheduler function with these parameters and get the URL
        error = None
        url = None
        try:
            url = parse_and_generate_url(year, semester, course_codes, whitelist)
        except ValueError as e:
            error = e

        return render_template('scheduler.html', url=url, error=error)
    else:
        return render_template('scheduler.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
