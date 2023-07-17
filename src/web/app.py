from flask import Flask, render_template, request, send_from_directory
from src.coursereg_history.api import get_all_data
from src.planner.cli import parse_and_generate_url
from argparse import ArgumentParser
import os

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/history', methods=['GET', 'POST'])
def history():
    year = '2324'
    semester = '1'
    type = 'ug'

    if request.method == 'POST':
        year = request.form.get('year')
        semester = request.form.get('semester')
        type = request.form.get('type')

    output = []
    error = None
    round_exists = []
    try:
        output = get_all_data(year, semester, type)
        for round_num in range(4):
            round_exists.append(
                    pdf_exists(f'{year}/{semester}/'
                               f'{type}/round_{round_num}.pdf'))
    except ValueError as e:
        error = e

    return render_template('history.html', output=output,
                           round_exists=round_exists, error=error)


pdf_directory = os.path.abspath(
        os.path.join(os.path.dirname(__file__),
                     '../coursereg_history/data/pdfs'))


def pdf_exists(filename):
    file_path = os.path.join(pdf_directory, filename)
    return os.path.isfile(file_path)


@app.route('/pdfs/<path:filename>')
def serve_pdf(filename):
    return send_from_directory(pdf_directory, filename)


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
