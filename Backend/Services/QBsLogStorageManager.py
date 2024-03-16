# ============================================================================================
# Log cleanup script that runs continuously to remove log files older than 5 days.

# Iterates through all files in the LOG_DIR directory and checks the modification
# time. If a log file is older than 5 days, it gets deleted.

# Runs indefinitely on a 24 hour interval.
# =============================================================================================


# =======================================================================
# Imports/Packages
# =======================================================================
import os
import sys
import time
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv
# Add the root directory to the Python path
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_dir)
from Config.PyLogger import RollingFileHandler

LOG_DIR = os.path.join(root_dir, 'Logs')

# Set up logging
script_dir = os.path.dirname(__file__)
env_path = os.path.join(script_dir, '..', '..', 'Config', '.env')
load_dotenv(env_path)
INTEGRATION_LOG_DIR = os.environ.get("INTEGRATION_LOG_DIR")
current_date = datetime.now().strftime('%Y-%m-%d')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler = RollingFileHandler(INTEGRATION_LOG_DIR, 'MenuFetcher.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


# ========================================================================================
# RemoveOldLogs() - Function to remove old logs from the LOG_DIR directory.
# ========================================================================================
def RemoveOldLogs():
    try:
        current_date = datetime.now()
        five_days_ago = current_date - timedelta(days=5)

        for filename in os.listdir(LOG_DIR):
            if filename.endswith(".log"):
                filepath = os.path.join(LOG_DIR, filename)
                mod_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                if mod_time < five_days_ago:
                    os.remove(filepath)
                    logging.info(f"Removed old log file: {filepath}")
    except Exception as e:
        logging.error(f"An error occurred while removing old log files: {e}")


if __name__ == "__main__":
    try:
        logging.info("Starting log cleanup script...")
        while True:
            RemoveOldLogs()
            logging.info(f"-- LogManagerService is alive {os.getpid()} --")
            logging.info("Sleeping for 24 hours...")
            time.sleep(24 * 60 * 60)
    except KeyboardInterrupt:
        logging.info("Script terminated by user.")
    except Exception as e:
        logging.error(f"Unexpected error occurred: \n{e}")
