import argparse
import os
import shutil
from pathlib import Path

from tabula.io import convert_into_by_batch
from src.history.util.PdfCsvMonitorer import PdfCsvMonitorer

TMP_DIRECTORY = "tmp_combined_pdfs" if not Path("/tmp").exists() else "/tmp/tmp_combined_pdfs"


def convert(pdf_files: list[str]) -> None:
    # Combine all PDFs into a single directory
    Path(TMP_DIRECTORY).mkdir(parents=True, exist_ok=True)
    for pdf_file in pdf_files:
        pdf_file_path = Path(pdf_file)
        # Extract the directory path
        file_dir = pdf_file_path.parent

        # Encode directory path with underscores and replace slashes
        encoded_dir = Path(str(file_dir).replace("/", "||"))

        # Extract the filename and extension
        filename, extension = pdf_file_path.stem, pdf_file_path.suffix

        # Construct the new filename
        new_filename = f"{encoded_dir}||{filename}{extension}"

        # Copy the file with the new name
        shutil.copy2(pdf_file, Path(TMP_DIRECTORY) / new_filename)

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
            (Path(TMP_DIRECTORY) / file).unlink()

    # Process each file in combined_pdfs directory
    for file in os.listdir(TMP_DIRECTORY):
        # Extract encoded directory and filename
        new_csv_file = "/".join(file.replace("pdfs", "raw").split("||"))
        new_file_dir = Path(new_csv_file).parent

        # Create the directory if needed
        Path(new_file_dir).mkdir(parents=True, exist_ok=True)

        # Move the file to the new location
        shutil.move(Path(TMP_DIRECTORY) / file, new_csv_file)

    # Delete the combined_pdfs directory
    shutil.rmtree(TMP_DIRECTORY)


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert PDFs to CSV")
    parser.add_argument("pdf_files", nargs="+", help="List of PDF files to convert")
    args = parser.parse_args()

    convert(args.pdf_files)


if __name__ == "__main__":
    main()
