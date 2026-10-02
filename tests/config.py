import os

from dotenv import load_dotenv

load_dotenv(
    override=False
)  # do not override variables that are already set (e.g. in CI)


class Config:
    APP_USERNAME = os.getenv("APP_USERNAME", "admin")
    APP_PASSWORD = os.getenv("APP_PASSWORD", "admin123")
    BASE_URL = os.getenv("BASE_URL", "http://localhost:8080")  # UI (nginx)
    API_URL = os.getenv("API_URL", "http://localhost:8000/api")  # backend directly
