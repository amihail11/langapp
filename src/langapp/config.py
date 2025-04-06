import os

from dotenv import load_dotenv

load_dotenv()

URL_DATABASE = os.getenv("URL_DATABASE")

if not URL_DATABASE:
    raise EnvironmentError("URL_DATABASE not found")
