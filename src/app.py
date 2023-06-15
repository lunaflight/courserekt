from flask import Flask, render_template, request
from main import get_data

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
