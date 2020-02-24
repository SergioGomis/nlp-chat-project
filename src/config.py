import os
import dotenv
from pathlib import Path  # python3 only
env_path = os.path.join(os.path.dirname(__file__), '.env')
print(env_path)
dotenv.load_dotenv(dotenv_path=env_path)


# Connect to the database
dbURL = os.getenv("MDB_URL")
if not dbURL:
    raise ValueError("You should specify MDB_URL environment variable")