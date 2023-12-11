# Project Structure

```
.
├── app.py
    - Flask application responsible for all web-related requests.
├── main.py
    - Entry point of the application.
├── precomp.py
    - Script responsible for generating all HTML pages statically beforehand.
├── static
    - Responsible for containing CSS, JS and assets.
└── templates
    - Jinja2 templates for generating the HTML webpages.
```

# Implementation

## Precomputing the HTML for Round Data

We do following to generate the HTML:

1. It queries `get_all_data()` from `src/history/api.py`.
2. It uses the returned value to generate the entire table using the HTML template with Jinja2.
3. The colouring of the table data is added by Jinja2 based on the ratio of availability.
4. We save it to the appropriate location under `static/pages/{YEAR}/{SEMESTER}/{TYPE}/index.html`.

## PDF Link Generation

1. The template checks if the directory for a specified YEAR, SEMESTER, UG/GD exists.
2. If it exists, it generates a link in the table header using the HTML template with Jinja2.

## Querying for new history data

The `<form>` tag encloses all year, semester and type data.
JavaScript detects if a new button is pressed, and sends a POST request which the Flask application immediately generates HTML from.

## Search Bar

The search bar does the following:
1. Every time new user input is detected, JS is immediately executed.
2. For every course, it is hidden if and only if the course code does not contain any of the filters, delimited by `' '`, as a substring.
   - It does so by adding `hidden` to the table row.

## Persistence
We use `localStorage` in JS to remember user input across different sessions while browsing data, for the following:
1. Search bar input
2. Toggle checkboxes
