import os

from dotenv import load_dotenv

load_dotenv()

MONGO_DB_NAME = "calorie_compass"
MONGO_HOST = os.environ["MONGO_HOST"]
MONGO_PORT = int(os.environ["MONGO_PORT"])
MONGO_USERNAME = os.environ["MONGO_USERNAME"]
MONGO_PASSWORD = os.environ["MONGO_PASSWORD"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
SECRET_KEY = os.environ["SECRET_KEY"]
