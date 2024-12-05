import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    # Argilla Configuration
    ARGILLA_API_URL = os.getenv("ARGILLA_API_URL")
    ARGILLA_API_KEY = os.getenv("ARGILLA_API_KEY")
    HF_TOKEN = os.getenv("HF_TOKEN")

    # User Credentials
    USER_PASSWORD = os.getenv("USER_PASSWORD")
