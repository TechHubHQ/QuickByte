import os
import sys
import time
import schedule
from dotenv import load_dotenv
from datetime import datetime
from subprocess import Popen
import logging

# Set up logging
script_dir = os.path.dirname(__file__)
env_path = os.path.join(script_dir, '..', '..', 'config', '.env')
load_dotenv(env_path)
BUILD_LOG_DIR = os.environ.get("BUILD_LOG_DIR")
current_date = datetime.now().strftime('%Y-%m-%d')
logging.basicConfig(
    filename=os.path.join(BUILD_LOG_DIR, f'{current_date}_RebuildEngine.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Add the root directory to the Python path
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_dir)

# Import necessary modules
from app import app
from Backend.Connections.QBcDBConnector import db
from Backend.Models.QBmLoadLocationID import CityLocation
from Backend.Models.QBmLoadRestaurantsByID import RestaurantsByLoc
from Backend.Models.QBmLoadMenu import MenuDetails

# Push the app context
env_path = os.path.join(root_dir, 'config', '.env')
load_dotenv(env_path)
app.app_context().push()

# Set up script directories
current_dir = os.path.dirname(os.path.abspath(__file__))
script_dir = os.path.join(current_dir, "..", "Integration")

loc_fetch_script = os.path.join(script_dir, "QBiLocationIDFetcher.py")
res_fetch_script = os.path.join(script_dir, "QBiRestaurantsFetcher.py")
menu_fetch_script = os.path.join(script_dir, "QBiMenuFetcher.py")


def empty_table(model):
    """Function to empty the given table"""
    model.query.delete()
    db.session.commit()
    logging.info(f"Table {model.__tablename__} emptied.")


def run_script(script_path, script_name):
    logging.info(f"Running {script_name}...")
    if script_name == 'QBiLocationIDFetcher.py':
        empty_table(CityLocation)
        start_time = time.time()
        process = Popen([sys.executable, script_path])
        process.wait()
        end_time = time.time()
        logging.info(f"{script_name} completed in {end_time - start_time:.2f} seconds.")
    elif script_name == 'QBiRestaurantsFetcher.py':
        empty_table(RestaurantsByLoc)
        start_time = time.time()
        process = Popen([sys.executable, script_path])
        process.wait()
        end_time = time.time()
        logging.info(f"{script_name} completed in {end_time - start_time:.2f} seconds.")
    elif script_name == 'QBiMenuFetcher.py':
        empty_table(MenuDetails)
        start_time = time.time()
        process = Popen([sys.executable, script_path])
        process.wait()
        end_time = time.time()
        logging.info(f"{script_name} completed in {end_time - start_time:.2f} seconds.")
    else:
        raise ValueError("Invalid script name")


# Define the time to run the scripts (7 am IST on Sundays)
schedule.every().sunday.at("07:00").do(lambda: run_script(loc_fetch_script, "Script 1"))
schedule.every().sunday.at("07:10").do(lambda: run_script(res_fetch_script, "Script 2"))
schedule.every().sunday.at("07:20").do(lambda: run_script(menu_fetch_script, "Script 3"))

# Check if the current day is Sunday and the current time is before 7 a.m.
if datetime.now().weekday() == 6 and datetime.now().hour == 7:
    run_script(loc_fetch_script, "QBiLocationIDFetcher.py")
    run_script(res_fetch_script, "QBiRestaurantsFetcher.py")
    run_script(menu_fetch_script, "QBiMenuFetcher.py")

# Keep the script running to schedule the jobs
while True:
    schedule.run_pending()
    time.sleep(10)

    # Log the PID and "Script is alive" if the script is running
    logging.info(f"PID: {os.getpid()} - QBbRebuildEngine is alive")

    # for Manual rebuild
    CORE_DEV = os.getenv("CORE_DEV")
    if len(sys.argv) > 1 and sys.argv[1] == "--rebuild" and sys.argv[2] in CORE_DEV:
        logging.info("----------------------------------------------")
        logging.info(f"Manual Rebuild process invoked by CORE DEV {sys.argv[2]}")
        logging.info("---------------------------------------------\n")
        run_script(loc_fetch_script, "QBiLocationIDFetcher.py")
        run_script(res_fetch_script, "QBiRestaurantsFetcher.py")
        run_script(menu_fetch_script, "QBiMenuFetcher.py")
        break
