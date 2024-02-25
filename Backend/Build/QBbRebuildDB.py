import os
import sys
import time
import schedule
from datetime import datetime
from subprocess import Popen
# Add the root directory to the Python path
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_dir)
from app import app
from Backend.Connections.QBcDBConnector import db
from Backend.Models.QBmLoadLocationID import CityLocation
from Backend.Models.QBmLoadRestaurantsByID import RestaurantsByLoc
from Backend.Models.QBmLoadMenu import MenuDetails

app.app_context().push()

current_dir = os.path.dirname(os.path.abspath(__file__))
script_dir = os.path.join(current_dir, "..", "Integration")

loc_fetch_script = os.path.join(script_dir, "QBiLocationIDFetcher.py")
res_fetch_script = os.path.join(script_dir, "QBiRestaurantsFetcher.py")
menu_fetch_script = os.path.join(script_dir, "QBiMenuFetcher.py")


def empty_table(model):
    """Function to empty the given table"""
    model.query.delete()
    db.session.commit()
    print(f"Table {model.__tablename__} emptied.")


def run_script(script_path, script_name):
    print(f"Running {script_name}...")

    if script_name == 'QBiLocationIDFetcher.py':
        empty_table(CityLocation)
        start_time = time.time()
        process = Popen([sys.executable, script_path])
        process.wait()
        end_time = time.time()
        print("\n------------------------------------------------------------------")
        print(f"{script_name} completed in {end_time - start_time:.2f} seconds.")
        print("------------------------------------------------------------------\n")
    elif script_name == 'QBiRestaurantsFetcher.py':
        empty_table(RestaurantsByLoc)
        start_time = time.time()
        process = Popen([sys.executable, script_path])
        process.wait()
        end_time = time.time()
        print("\n------------------------------------------------------------------")
        print(f"{script_name} completed in {end_time - start_time:.2f} seconds.")
        print("------------------------------------------------------------------\n")
    elif script_name == 'QBiMenuFetcher.py':
        empty_table(MenuDetails)
        start_time = time.time()
        process = Popen([sys.executable, script_path])
        process.wait()
        end_time = time.time()
        print("\n------------------------------------------------------------------")
        print(f"{script_name} completed in {end_time - start_time:.2f} seconds.")
        print("------------------------------------------------------------------\n")
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
    time.sleep(1)

    # Print the PID and "Script is alive" if the script is running
    print(f"PID: {os.getpid()} - QBbRebuildDB is alive")

    # If the process is invoked by a rebuild, print the process
    if len(sys.argv) > 1 and sys.argv[1] == "--rebuild":
        print("\n--------------------------------------------")
        print("Rebuild process invoked")
        print("---------------------------------------------\n")
        run_script(loc_fetch_script, "QBiLocationIDFetcher.py")
        run_script(res_fetch_script, "QBiRestaurantsFetcher.py")
        run_script(menu_fetch_script, "QBiMenuFetcher.py")
        break
