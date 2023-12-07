import logging
import os
from pathlib import Path

from dotenv import load_dotenv

file_name = os.getenv("ENV_FILE_PATH", "./.env")
print(f"Loading env file: {file_name}")
load_dotenv(file_name)

MONGO_DB_NAME = "calorie_compass"
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = int(os.getenv("MONGO_PORT", "0"))
MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
AZURE_ACCOUNT = "cs2100320026d49969e"
AZURE_CONN = os.getenv("AZURE_CONN")
AZURE_CONTAINER = os.getenv("AZURE_CONTAINER")

LOG_FORMAT = "%(asctime)s:%(name)s:%(levelname)s - %(message)s"
CONSOLE_LOG_FORMAT = "%(asctime)s:%(name)s:%(levelname)s - %(message)s"
logging.basicConfig(
    level=logging.ERROR,
    format=LOG_FORMAT,
)

CURRENT_DIRECTORY: Path = Path(__file__).parent
BASE_DIRECTORY = CURRENT_DIRECTORY.parent.absolute()
