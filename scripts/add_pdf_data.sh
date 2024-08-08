#!/bin/bash

# Ensure arguments are provided
if [ $# -ne 3 ]; then
  echo "Usage: $0 ACAD_YEAR SEMESTER ROUND"
  exit 1
fi

# Assign arguments to variables
ACAD_YEAR=$1
SEMESTER=$2
ROUND=$3

# Prompt user to download PDFs
echo "Please visit the following URLs to download PDFs and save them in the current directory:"
echo "https://nus.edu.sg/coursereg/docs/VacancyRpt_R${ROUND}.pdf"
echo "https://www.nus.edu.sg/CourseReg/docs/DemandAllocationRptUG_R${ROUND}.pdf"
echo "https://www.nus.edu.sg/CourseReg/docs/DemandAllocationRptGD_R${ROUND}.pdf"
echo "**NOTE:** Downloading using curl is disabled due to firewall issues."
echo "Press 'y' when you are done downloading all PDFs."

read -r -p "Press y to continue: " response
if [[ ! $response =~ ^([Yy])$ ]]; then
  echo "Exiting script. Please ensure all PDFs are downloaded before continuing."
  exit 1
fi

# Create directories if they don't exist
mkdir -p src/history/vacancy_history/data/pdfs/"$ACAD_YEAR"/"$SEMESTER"
mkdir -p src/history/coursereg_history/data/pdfs/"$ACAD_YEAR"/"$SEMESTER"/ug
mkdir -p src/history/coursereg_history/data/pdfs/"$ACAD_YEAR"/"$SEMESTER"/gd

# Move downloaded PDFs
mv VacancyRpt_R"$ROUND".pdf src/history/vacancy_history/data/pdfs/"$ACAD_YEAR"/"$SEMESTER"/round_"$ROUND".pdf
mv DemandAllocationRptUG_R"$ROUND".pdf src/history/coursereg_history/data/pdfs/"$ACAD_YEAR"/"$SEMESTER"/ug/round_"$ROUND".pdf
mv DemandAllocationRptGD_R"$ROUND".pdf src/history/coursereg_history/data/pdfs/"$ACAD_YEAR"/"$SEMESTER"/gd/round_"$ROUND".pdf

# Activate virtual environment and run script
source venv/bin/activate
python -m src.history.build --year "$ACAD_YEAR" --semester "$SEMESTER"
deactivate
