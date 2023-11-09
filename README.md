# backend

## Setup:

To setup on a local environment:

- Install the dependencies
  `pip install -r requirements.txt2` (make sure you enable virtual environment if any)
- Run the app:
    `python main.py` or `export FLASK_APP=api` then `flask run`

### Local Environment

To run locally without a remote MONGO, need to have a local MongoDB.
The easiest way is to use docker.
After installing docker, run the command from the `start_db.sh`
file.
To start or stop the DB, just use `docker start/stop local_mongo`
