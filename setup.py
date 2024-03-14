import os
import sqlite3
import subprocess

# Create the DATABASE directory if it doesn't exist
DB_dir = "DataBase"
if not os.path.exists(DB_dir):
    os.makedirs(DB_dir)

# Create the SQLite database file inside the directory
db_path = os.path.join(DB_dir, "QB.db")
if not os.path.exists(db_path):
    with sqlite3.connect(db_path) as conn:
        print(f"SQLite database file '{db_path}' created successfully.")
else:
    print(f"SQLite database file '{db_path}' already exists.")


# Create the Image directory if it doesn't exist
img_dir = "Frontend/Static/Images/"

image_folder_path = os.path.join(img_dir, "Users")

if not os.path.exists(image_folder_path):
    os.makedirs(image_folder_path)
    print(f"Image folder '{image_folder_path}' created successfully.")


# Create LOG directories if they don't exist
LOG_dir = "Logs"
if not os.path.exists(LOG_dir):
    os.makedirs(LOG_dir)
    print(f"LOG directory '{LOG_dir}' created successfully.")

APP_LOG_dir = os.path.join(LOG_dir, "APP")
if not os.path.exists(APP_LOG_dir):
    os.makedirs(APP_LOG_dir)
    print(f"APP LOG directory '{APP_LOG_dir}' created successfully.")

INTEGRATION_LOG_dir = os.path.join(LOG_dir, "INTEGRATIONS")
if not os.path.exists(INTEGRATION_LOG_dir):
    os.makedirs(INTEGRATION_LOG_dir)
    print(f"INTEGRATION LOG directory '{INTEGRATION_LOG_dir}' created successfully.")

LOGIC_LOG_dir = os.path.join(LOG_dir, "LOGIC")
if not os.path.exists(LOGIC_LOG_dir):
    os.makedirs(LOGIC_LOG_dir)
    print(f"LOGIC LOG directory '{LOGIC_LOG_dir}' created successfully.")

SERVICES_LOG_dir = os.path.join(LOG_dir, "SERVICES")
if not os.path.exists(SERVICES_LOG_dir):
    os.makedirs(SERVICES_LOG_dir)
    print(f"SERVICES LOG directory '{SERVICES_LOG_dir}' created successfully.")

# Install required Python packages from requirements.txt
requirements_file = "requirements.txt"
if os.path.exists(requirements_file):
    with open(requirements_file, "r") as f:
        packages = f.read().splitlines()
        subprocess.run(["pip", "install", *packages])
        print("Requirements installed successfully.")
else:
    print(f"Could not find '{requirements_file}' in the root directory.")

print("Setup complete.")
