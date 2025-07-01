# ============================================================================================
# Log cleanup script that runs continuously to remove log files older than 5 days.

# Iterates through all directories inside the LOG_DIR directory and checks the modification
# time of files.
# If a log file is older than 5 days, it gets deleted.

# Runs indefinitely on a 24 hour interval.
# =============================================================================================

# =======================================================================
# Imports/Packages
# =======================================================================
from Config.PyLogger import RollingFileHandler
import os
import sys
import time
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Add the root directory to the Python path
root_dir = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_dir)

LOG_DIR = os.path.join(root_dir, 'Logs')

# Set up logging
script_dir = os.path.dirname(__file__)
env_path = os.path.join(script_dir, '..', '..', 'Config', '.env')
load_dotenv(env_path)
SERVICES_LOG_DIR = os.environ.get("SERVICES_LOG_DIR")
current_date = datetime.now().strftime('%Y-%m-%d')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler = RollingFileHandler(SERVICES_LOG_DIR, 'LogManager.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


# ========================================================================================
# RemoveOldLogs() - Function to remove old logs from all directories inside the LOG_DIR.
# ========================================================================================
def RemoveOldLogs():
    try:
        current_date = datetime.now()
        five_days_ago = current_date - timedelta(days=5)

        for root, _, files in os.walk(LOG_DIR):
            for filename in files:
                if filename.endswith(".log"):
                    filepath = os.path.join(root, filename)
                    mod_time = datetime.fromtimestamp(
                        os.path.getmtime(filepath))
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
