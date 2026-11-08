import os
from pathlib import Path

from dotenv import load_dotenv

# Корневая папка проекта
BASE_DIR = Path(__file__).resolve().parent

# Загружаем переменные из .env
load_dotenv(BASE_DIR / ".env")


class Config:
    # Безопасность Flask
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")

    # База данных SQLite
    SQLALCHEMY_DATABASE_URI = (
        f"sqlite:///{BASE_DIR / 'instance' / 'spendly.db'}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Telegram Bot
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    # Настройки приложения
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"