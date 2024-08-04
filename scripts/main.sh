#!/bin/bash

main ()
{
    python -m src.web.main
}

source venv/bin/activate
main
deactivate
