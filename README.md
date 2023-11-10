# backend

## Setup:

To setup on a local environment:

- Install the dependencies
  `pip install -r requirements.txt` (make sure you enable virtual environment if any)
- Run the app:
    `python main.py` or `export FLASK_APP=api` then `flask run`
  
- Make sure there is a valid .env file in the repository. Look at the .env_example to see what is needed.

### Local Environment

To run locally without a remote MONGO, need to have a local MongoDB.
The easiest way is to use docker.
After installing docker, run the command from the `start_db.sh`
file.
To start or stop the DB, just use `docker start/stop local_mongo`
