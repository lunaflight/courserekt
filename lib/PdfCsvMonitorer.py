import logging
from pathlib import Path
from threading import Thread
from time import sleep


class PdfCsvMonitorer(Thread):
    def __init__(self, directory: str, update_freq: int = 1) -> None:
        """Monitor progress of PDF to CSV conversion."""
        self.directory = Path(directory)
        self.update_freq = update_freq
        self.logger = logging.getLogger("PdfCsvMonitorer")

        super().__init__()
        self.running = True
        self.logger.debug("Init completed.")

    def run(self) -> None:
        """Tracks pdf to csv conversion."""
        prev_csv_cnt: int = -1

        while self.running:
            csv_files_cnt: int = sum([1 for _ in self.directory.glob("*.csv")])
            pdf_files_cnt: int = sum([1 for _ in self.directory.glob("*.pdf")])

            if prev_csv_cnt != csv_files_cnt:
                self.logger.info("Converting PDFs to CSVs... %s/%s",
                                 csv_files_cnt, pdf_files_cnt)

            prev_csv_cnt = csv_files_cnt
            sleep(1/self.update_freq)

    def stop(self) -> None:
        """Terminates thread."""
        self.running = False
        self.join()  # properly terminate thread (occurs only after sleep ends)
        self.logger.debug("Stop completed.")
