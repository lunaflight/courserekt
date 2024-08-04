#!/bin/bash

main ()
{
    python -m unittest &&
    python -m mypy --strict . &&
    python -m ruff check --statistics
}

source venv/bin/activate
main
deactivate
