# backend

## Setup:

To setup on a local environment:

- Install the dependencies
  `pip install -r requirements.txt` (make sure you enable virtual environment if any)
- Run the app:
  `python main.py` or `export FLASK_APP=api` then `flask run`

- Make sure there is a valid .env file in the repository. Look at the `env_example` to see what is needed, or just change the name of `env_example` to .env
  Alternatively, you can set ENV_FILE_PATH with any env file as follows: `export ENV_FILE_PATH="./test_env"`
  The app will take the `test_env` file as you instructed. The app prints the file name before loading, so it is easy to
  verify the app took the correct file. Testing with pytest uses the same mechanism.

### Local Environment

To run locally without a remote MONGO, need to have a local MongoDB. The easiest way is to use docker. After installing
docker, run the command from the `start_db.sh`
file. To start or stop the DB, just use `docker start/stop local_mongo`
