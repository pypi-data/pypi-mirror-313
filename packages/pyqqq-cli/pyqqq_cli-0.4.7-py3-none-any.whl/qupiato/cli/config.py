import dotenv
import os

dotenv.load_dotenv(dotenv.find_dotenv())


PYQQQ_API_KEY = os.getenv("PYQQQ_API_KEY")

BUCKET_NAME = "qupiato-user-artifacts"

DEPLOYER_WS_URL = os.getenv("DEPLOYER_WS_URL", "wss://qupiato.com/deployer/ws")

CREDENTIAL_FILE_PATH = os.path.expanduser("~/.qred")

API_SERVER_URL = os.getenv("API_SERVER_URL", "https://qupiato.com/api")
