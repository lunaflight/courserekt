from flask import Flask, render_template, request
from src.coursereg_history.api import get_data
from src.planner.cli import parse_and_generate_url

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/history', methods=['GET', 'POST'])
def history():
    if request.method == 'POST':
        year = request.form.get('year')
        semester = request.form.get('semester')
        type = request.form.get('type')
        course_codes = request.form.get('course_codes').split()

        output = []
        errors = []
        for course_code in course_codes:
            try:
                output.append(get_data(year, semester, type, course_code))
            except ValueError as e:
                errors.append(e)

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

        error = None
        url = None
        try:
            url = parse_and_generate_url(year, semester,
                                         course_codes, whitelist)
        except ValueError as e:
            error = e

        return render_template('scheduler.html', url=url, error=error)
    else:
        return render_template('scheduler.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
