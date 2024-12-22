import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000").strip("/")
