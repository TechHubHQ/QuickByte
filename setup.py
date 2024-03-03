import os
import sqlite3
import subprocess

# Create the directory if it doesn't exist
directory = "DataBase"
if not os.path.exists(directory):
    os.makedirs(directory)

# Create the SQLite database file inside the directory
db_path = os.path.join(directory, "QB.db")
if not os.path.exists(db_path):
    with sqlite3.connect(db_path) as conn:
        print(f"SQLite database file '{db_path}' created successfully.")
else:
    print(f"SQLite database file '{db_path}' already exists.")

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
