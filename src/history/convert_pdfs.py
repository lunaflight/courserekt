import argparse
import os
import tabula


def main(pdf_files):
    for pdf_file in pdf_files:
        if not os.path.exists(pdf_file):
            raise FileNotFoundError(f"PDF file not found: {pdf_file}")

        # Get the base name of the file (without directory or extension)
        base_name = os.path.basename(pdf_file).split(".")[0]

        # Get the base directory path
        base_dir = os.path.dirname(pdf_file)

        # Replace "pdfs" with "raw" in the base directory path
        output_dir = base_dir.replace("pdfs", "raw")

        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # The path to the output CSV file
        output_file = os.path.join(output_dir, f"{base_name}.csv")

        # Run tabula command using tabula library
        tabula.convert_into(
            pdf_file,
            output_file,
            output_format="csv",
            pages="all",
            lattice=True,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PDFs to CSV")
    parser.add_argument("pdf_files", nargs="+", help="List of PDF files to convert")
    args = parser.parse_args()

    main(args.pdf_files)
