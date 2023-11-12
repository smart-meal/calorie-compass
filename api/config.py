import logging
import os
from pathlib import Path

from dotenv import load_dotenv

file_name = os.getenv("ENV_FILE_PATH", "./.env")
print(f"Loading env file: {file_name}")
load_dotenv(file_name)

MONGO_DB_NAME = "calorie_compass"
MONGO_HOST = os.environ["MONGO_HOST"]
MONGO_PORT = int(os.environ["MONGO_PORT"])
MONGO_USERNAME = os.environ["MONGO_USERNAME"]
MONGO_PASSWORD = os.environ["MONGO_PASSWORD"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
SECRET_KEY = os.environ["SECRET_KEY"]

LOG_FORMAT = "%(asctime)s:%(name)s:%(levelname)s - %(message)s"
CONSOLE_LOG_FORMAT = "%(levelname)s - %(message)s"
logging.basicConfig(
    level=logging.ERROR,
    format=LOG_FORMAT,
)

CURRENT_DIRECTORY: Path = Path(__file__).parent
BASE_DIRECTORY = CURRENT_DIRECTORY.parent.absolute()
