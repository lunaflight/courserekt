## Project Structure

```
.
├── app.py
    - Flask application responsible for the '/' directory.
├── static
    - Responsible for containing CSS, JS and assets.
└── templates
    - Jinja2 templates for generating the HTML webpages.
```

## Implementation

### Round Data Generation

The Flask application does the following to generate the HTML:

1. It queries `get_all_data()` from `src/coursereg_history/api.py`.
2. It uses the returned value to generate the entire table using the HTML template with Jinja2.
3. The colouring of the table data is added by Jinja2 based on the ratio of availability.

### PDF Link Generation

1. The template checks if the directory for a specified YEAR, SEMESTER, UG/GD exists.
    - TODO: This should probably be handled by `api.py` with `check_exists()`.
2. If it exists, it generates a link in the table header using the HTML template with Jinja2.

### Querying for new history data

The `<form>` tag encloses all year, semester and type data.
JavaScript detects if a new button is pressed, and sends a POST request which the Flask application immediately generates HTML from.

### Search Bar

The search bar does the following:
1. Every time new user input is detected, JS is immediately executed.
2. For every course, it is hidden if and only if the course code does not contain any of the filters, delimited by `' '`, as a substring.
   - It does so by adding `hidden` to the table row.
