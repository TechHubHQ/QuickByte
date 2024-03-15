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
import time
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Set up logging
script_dir = os.path.dirname(__file__)
env_path = os.path.join(script_dir, '..', '..', 'Config', '.env')
load_dotenv(env_path)
SERVICE_LOG_DIR = os.environ.get("SERVICES_LOG_DIR")
current_date = datetime.now().strftime('%Y-%m-%d')
logging.basicConfig(
    filename=os.path.join(SERVICE_LOG_DIR, f'{current_date}_LogManagerService.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Add the root directory to the Python path
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

LOG_DIR = os.path.join(root_dir, 'Logs')


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
