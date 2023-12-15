import argparse
import os
import shutil
from tabula.io import convert_into_by_batch
from typing import List


def main(pdf_files: List[str]) -> None:
    # Combine all PDFs into a single directory
    target_dir = "combined_pdfs"
    os.makedirs(target_dir, exist_ok=True)
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
        shutil.copy2(pdf_file, os.path.join(target_dir, new_filename))

    # Run tabula conversion on the combined directory
    convert_into_by_batch(
        target_dir,
        output_format="csv",
        pages="all",
        lattice=True,
    )

    # Remove all PDFs
    for file in os.listdir(target_dir):
        # Check if the file extension is .pdf
        if file.endswith(".pdf"):
            # Delete the file
            os.remove(os.path.join(target_dir, file))

    # Process each file in combined_pdfs directory
    for file in os.listdir(target_dir):
        # Extract encoded directory and filename
        new_csv_file = "/".join(file.replace("pdfs", "raw").split("||"))
        new_file_dir = os.path.dirname(new_csv_file)

        # Create the directory if needed
        os.makedirs(new_file_dir, exist_ok=True)

        # Move the file to the new location
        shutil.move(os.path.join(target_dir, file), new_csv_file)

    # Delete the combined_pdfs directory
    shutil.rmtree(target_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PDFs to CSV")
    parser.add_argument("pdf_files", nargs="+", help="List of PDF files to convert")
    args = parser.parse_args()

    main(args.pdf_files)
