import argparse
import os
import shutil

from tabula.io import convert_into_by_batch
from src.history.util.PdfCsvMonitorer import PdfCsvMonitorer

TMP_DIRECTORY = "tmp_combined_pdfs"


def convert(pdf_files: list[str]) -> None:
    # Combine all PDFs into a single directory
    os.makedirs(TMP_DIRECTORY, exist_ok=True)
    for pdf_file in pdf_files:
        # Extract the directory path
        file_dir = os.path.dirname(pdf_file)

        # Encode directory path with underscores and replace slashes
        encoded_dir = file_dir.replace("/", "||")

        # Extract the filename and extension
        filename, extension = os.path.splitext(os.path.basename(pdf_file))

        # Construct the new filename
        new_filename = f"{encoded_dir}||{filename}{extension}"

        # Copy the file with the new name
        shutil.copy2(pdf_file, os.path.join(TMP_DIRECTORY, new_filename))

    monitorer = PdfCsvMonitorer(TMP_DIRECTORY)

    # Run tabula conversion on the combined directory
    monitorer.start()
    convert_into_by_batch(
        TMP_DIRECTORY,
        output_format="csv",
        pages="all",
        lattice=True,
    )
    monitorer.stop()

    # Remove all PDFs
    for file in os.listdir(TMP_DIRECTORY):
        # Check if the file extension is .pdf
        if file.endswith(".pdf"):
            # Delete the file
            os.remove(os.path.join(TMP_DIRECTORY, file))

    # Process each file in combined_pdfs directory
    for file in os.listdir(TMP_DIRECTORY):
        # Extract encoded directory and filename
        new_csv_file = "/".join(file.replace("pdfs", "raw").split("||"))
        new_file_dir = os.path.dirname(new_csv_file)

        # Create the directory if needed
        os.makedirs(new_file_dir, exist_ok=True)

        # Move the file to the new location
        shutil.move(os.path.join(TMP_DIRECTORY, file), new_csv_file)

    # Delete the combined_pdfs directory
    shutil.rmtree(TMP_DIRECTORY)


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert PDFs to CSV")
    parser.add_argument("pdf_files", nargs="+", help="List of PDF files to convert")
    args = parser.parse_args()

    convert(args.pdf_files)


if __name__ == "__main__":
    main()
