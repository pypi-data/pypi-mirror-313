import os

from dotenv import load_dotenv

load_dotenv()


def get_dotenv(key: str) -> str | None:
    return os.getenv(key)
