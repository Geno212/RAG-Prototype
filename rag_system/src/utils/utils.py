import os
import logging
import shutil
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_directory(directory: str) -> None:
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info(f"Created directory: {directory}")

def cleanup_temp_files(directory: str, max_age: int = 24) -> None:
    max_age_time = datetime.now() - timedelta(hours=max_age)
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path) and datetime.fromtimestamp(os.path.getmtime(file_path)) < max_age_time:
            os.remove(file_path)
            logging.info(f"Deleted old temporary file: {file_path}")
