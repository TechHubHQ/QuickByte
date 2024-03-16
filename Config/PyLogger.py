# ====================================================================
# This script handles logging and manages the log files
# ====================================================================

# ===================================================
# Imports/Packages
# ===================================================
import os
from datetime import datetime
import logging


class RollingFileHandler(logging.FileHandler):
    def __init__(self, log_dir, log_file_name, mode='a', encoding=None, delay=False):
        self.log_dir = log_dir
        self.log_file_name = log_file_name
        self.current_date = datetime.now().date()
        self.baseFilename = self.get_log_file_path()
        super().__init__(self.baseFilename, mode, encoding, delay)

    def get_log_file_path(self):
        current_date = datetime.now().date()
        if current_date != self.current_date:
            self.current_date = current_date
            self.baseFilename = os.path.join(self.log_dir, f'{current_date:%Y-%m-%d}_{self.log_file_name}')
        return self.baseFilename

    def emit(self, record):
        self.stream = self._open()
        logging.StreamHandler.emit(self, record)
        self.flush()
        self.close()
