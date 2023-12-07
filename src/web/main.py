from argparse import ArgumentParser
from src.web.app import app
from src.web.precomp import generate_pages


def main():
    parser = ArgumentParser(description='Web app for CourseRekt')
    parser.add_argument('--port', type=int, nargs=1, default=5000,
                        help='Port where the app is run.')
    args = parser.parse_args()

    generate_pages()
    app.run(host='0.0.0.0', port=args.port, debug=True)


if __name__ == "__main__":
    main()
