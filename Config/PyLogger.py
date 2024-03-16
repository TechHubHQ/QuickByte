<<<<<<< HEAD
# ====================================================================
# This script handles logging and manages the log files
# ====================================================================

# ===================================================
# Imports/Packages
# ===================================================
=======
# =================================================================================================
# This is a modified version of the logging.FileHandler class
# =================================================================================================

# ========================================================
# Imports/Packages
# ========================================================
>>>>>>> 0b86a1e4c86dbbe8dc009082d3a0baab1cbd0032
import os
from datetime import datetime
import logging


class RollingFileHandler(logging.FileHandler):
    def __init__(self, log_dir, log_file_name, mode='a', encoding=None, delay=False):
        self.log_dir = log_dir
        self.log_file_name = log_file_name
        self.current_date = datetime.now().date()
<<<<<<< HEAD
        self.baseFilename = self.get_log_file_path()
        super().__init__(self.baseFilename, mode, encoding, delay)
=======
        super().__init__(self.get_log_file_path(), mode, encoding, delay)
>>>>>>> 0b86a1e4c86dbbe8dc009082d3a0baab1cbd0032

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
