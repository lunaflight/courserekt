#!/bin/bash

main ()
{
    pip install -r local-requirements.txt &&
    python -m src.history.build
}

# Create virtual environment
python3.12 -m venv venv
if [ $? -ne 0 ]; then
  echo "Error creating virtual environment"
  exit 1
fi

source venv/bin/activate
main
deactivate
