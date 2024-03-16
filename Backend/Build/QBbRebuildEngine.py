# ======================================================================================================================
# This script is designed to automate the process of fetching and updating data from external APIs into the database.
# It performs the following tasks:

# 1. Sets up logging and loads environment variables from a .env file.
# 2. Adds the root directory to the system path and imports the necessary modules.
# 3. Initializes the Flask application context and creates the database tables if they don't exist.
# 4. Defines helper functions to empty database tables and run external scripts.
# 5. Schedules three external scripts to run at specific times on Sundays using the `schedule` library:
#    - QBiLocationIDFetcher.py: Fetches location IDs for cities.
#    - QBiRestaurantsFetcher.py: Fetches restaurant data for the fetched locations.
#    - QBiMenuFetcher.py: Fetches menu details for the fetched restaurants.
# 6. Checks if the current day is Sunday and the current time is before 7 a.m. If so, it runs the three scripts.
# 7. Enters an infinite loop where it:
#    - Runs any pending scheduled tasks.
#    - Logs the process ID and a message indicating the script is alive.
#    - Checks for a manual rebuild command (`--rebuild`) passed as an argument. If present and the user is listed as
#      a core developer, it runs the three scripts and exits.
# 8. The script continues running until explicitly terminated, allowing the scheduled tasks to execute at the specified
#    times on Sundays or when manually invoked.

# This script orchestrates the data fetching and updating process by scheduling and running external scripts at specific
# times or on-demand, ensuring that the database is kept up-to-date with the latest data from external APIs.
# =======================================================================================================================

# =============================================================
# Imports/Packages
# =============================================================

import os
import sys
import time
import schedule
from dotenv import load_dotenv
from datetime import datetime
from subprocess import Popen
import logging
# Add the root directory to the Python path
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_dir)

# Import necessary modules
from app import app
from Backend.Connections.QBcDBConnector import db
from Backend.Models.QBmLoadLocationID import CityLocation
from Backend.Models.QBmLoadRestaurantsByID import RestaurantsByLoc
from Backend.Models.QBmLoadMenu import MenuDetails
from Config.PyLogger import RollingFileHandler

# Set up logging
script_dir = os.path.dirname(__file__)
env_path = os.path.join(script_dir, '..', '..', 'Config', '.env')
load_dotenv(env_path)
BUILD_LOG_DIR = os.environ.get("BUILD_LOG_DIR")
current_date = datetime.now().strftime('%Y-%m-%d')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler = RollingFileHandler(BUILD_LOG_DIR, 'RebuildEngine.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Push the app context
app.app_context().push()

# Set up script directories
current_dir = os.path.dirname(os.path.abspath(__file__))
script_dir = os.path.join(current_dir, "..", "Integration")

loc_fetch_script = os.path.join(script_dir, "QBiLocationIDFetcher.py")
res_fetch_script = os.path.join(script_dir, "QBiRestaurantsFetcher.py")
menu_fetch_script = os.path.join(script_dir, "QBiMenuFetcher.py")


# =================================================================
# EmptyTable --> removes all records from the given database table.
# =================================================================
def EmptyTable(model):
    """
    Removes all records from the given database table.

    Args:
        model: The SQLAlchemy model class corresponding to the table to be emptied.

    This function uses the provided model class to query and delete all records from the corresponding table.
    After deleting the records, it commits the changes to the database.

    It logs a message indicating that the table has been emptied.
    """
    
    model.query.delete()
    db.session.commit()
    logging.info(f"Table {model.__tablename__} emptied.")


# ===================================================================
# RunScript --> runs the specified external script and logs the time.
# ===================================================================

def RunScript(script_path, script_name):
    """
    Runs the specified external script and logs the execution time.

    Args:
        script_path (str): The file path of the script to be executed.
        script_name (str): The name of the script being executed.

    This function first empties the corresponding database table(s) based on the script_name.
    It then starts a subprocess to execute the script using the specified script_path.
    The function waits for the subprocess to complete and logs the execution time.

    If an invalid script_name is provided, it raises a ValueError.
    """
    
    logging.info(f"Running {script_name}...")
    if script_name == 'QBiStdAloneLocFetcher.py':
        EmptyTable(CityLocation)
        start_time = time.time()
        process = Popen([sys.executable, script_path])
        process.wait()
        end_time = time.time()
        logging.info(f"{script_name} completed in {end_time - start_time:.2f} seconds.")
    elif script_name == 'QBiRestaurantsFetcher.py':
        EmptyTable(RestaurantsByLoc)
        start_time = time.time()
        process = Popen([sys.executable, script_path])
        process.wait()
        end_time = time.time()
        logging.info(f"{script_name} completed in {end_time - start_time:.2f} seconds.")
    elif script_name == 'QBiMenuFetcher.py':
        EmptyTable(MenuDetails)
        start_time = time.time()
        process = Popen([sys.executable, script_path])
        process.wait()
        end_time = time.time()
        logging.info(f"{script_name} completed in {end_time - start_time:.2f} seconds.")
    else:
        raise ValueError("Invalid script name")


# Define the time to run the scripts (7 am IST on Sundays)
schedule.every().sunday.at("07:00").do(lambda: RunScript(loc_fetch_script, "Script 1"))
schedule.every().sunday.at("07:10").do(lambda: RunScript(res_fetch_script, "Script 2"))
schedule.every().sunday.at("07:20").do(lambda: RunScript(menu_fetch_script, "Script 3"))

# Check if the current day is Sunday and the current time is before 7 a.m.
if datetime.now().weekday() == 6 and datetime.now().hour == 7:
    RunScript(loc_fetch_script, "QBiStdAloneLocFetcher.py")
    RunScript(res_fetch_script, "QBiRestaurantsFetcher.py")
    RunScript(menu_fetch_script, "QBiMenuFetcher.py")

# Keep the script running to schedule the jobs
while True:
    schedule.run_pending()
    time.sleep(10)

    # Log the PID and "Script is alive" if the script is running
    logging.info(f"PID: {os.getpid()} - QBbRebuildEngine is alive")

    # for Manual rebuild
    CORE_DEV = os.getenv("CORE_DEV")
    if len(sys.argv) > 1 and sys.argv[1] == "--rebuild" and sys.argv[2] in CORE_DEV:
        logging.info("-----------------------------------------------------------")
        logging.info(f"Manual Rebuild process invoked by CORE DEV {sys.argv[2]}")
        logging.info("---------------------------------------------------------\n")
        RunScript(loc_fetch_script, "QBiLocationIDFetcher.py")
        RunScript(res_fetch_script, "QBiRestaurantsFetcher.py")
        RunScript(menu_fetch_script, "QBiMenuFetcher.py")
        break
