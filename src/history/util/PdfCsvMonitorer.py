import os
from threading import Thread
from time import sleep


class PdfCsvMonitorer(Thread):
    def __init__(self, directory: str, update_freq: int = 1) -> None:
        self.directory = directory
        self.update_freq = update_freq

        Thread.__init__(self)
        self.running = True

    def run(self) -> None:
        prev_csv_cnt: int = -1

        while self.running:
            csv_files: list[str] = [file for file in os.listdir(self.directory) if file.endswith(".csv")]
            pdf_files: list[str] = [file for file in os.listdir(self.directory) if file.endswith(".pdf")]
            csv_files_cnt: int = len(csv_files)
            pdf_files_cnt: int = len(pdf_files)

            if prev_csv_cnt != csv_files_cnt:
                print(f"Converting PDFs to CSVs... {csv_files_cnt}/{pdf_files_cnt}")

            prev_csv_cnt = csv_files_cnt
            sleep(1)

    def stop(self) -> None:
        self.running = False
