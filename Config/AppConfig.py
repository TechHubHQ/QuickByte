import os
from dotenv import load_dotenv
from datetime import datetime

script_dir = os.path.dirname(__file__)
env_path = os.path.join(script_dir, '.env')
load_dotenv(env_path)

current_date = datetime.now().strftime("%Y-%m-%d")


class Config:
    DB = os.environ.get('DB')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    UPLOAD_FOLDER_RELATIVE = os.environ.get('UPLOAD_FOLDER_RELATIVE')
    QR_FOLDER_RELATIVE = os.environ.get('QRCODE_FOLDER_RELATIVE')
    APP_LOG_FOLDER = os.environ.get('APP_LOG_FOLDER')
    INTEGRATION_LOG_FOLDER = os.environ.get('INTEGRATION_LOG_FOLDER')
    LOGIC_LOG_FOLDER = os.environ.get('LOGIC_LOG_FOLDER')
    SERVICES_LOG_FOLDER = os.environ.get('SERVICES_LOG_FOLDER')
    APP_LOG_FILE = f"{APP_LOG_FOLDER}/{current_date}_QUICK-BYTE.log"
