from flask import Flask, render_template, request
from src.coursereg_history.api import get_data, get_all_data
from src.planner.cli import parse_and_generate_url
from argparse import ArgumentParser

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

        return render_template('history.html', output=get_all_data(year, semester, type))
    else:
        return render_template('history.html', output=get_all_data('2324', 1, 'ug'))


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
    parser = ArgumentParser(description='Web app for NUS Tools')
    parser.add_argument('--port', type=int, nargs=1, default=5000,
                        help='Port where the app is run.')
    args = parser.parse_args()

    app.run(host='0.0.0.0', port=args.port, debug=True)
