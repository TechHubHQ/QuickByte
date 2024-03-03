import os
from dotenv import load_dotenv

script_dir = os.path.dirname(__file__)
env_path = os.path.join(script_dir, '.env')
load_dotenv(env_path)


class Config:
    DB = os.environ.get('DB')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    UPLOAD_FOLDER_RELATIVE = os.environ.get('UPLOAD_FOLDER_RELATIVE')
