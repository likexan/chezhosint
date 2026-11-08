from pathlib import Path

from flask import Flask, jsonify, render_template

from config import Config
from extensions import db

from routes.auth import auth_bp

# Импортируем модели, чтобы SQLAlchemy зарегистрировал их
from models import User, Subscription, Category, Payment


def create_app():
    app = Flask(__name__)

    # Загружаем настройки
    app.config.from_object(Config)

    # Создаём папку для базы данных, если её нет
    Path(app.instance_path).mkdir(
        parents=True,
        exist_ok=True
    )

    # Подключаем базу данных
    db.init_app(app)

    app.register_blueprint(auth_bp)

    # Главная страница
    @app.route("/")
    def index():
        return render_template("index.html")

    # Проверка состояния сервера
    @app.route("/api/health")
    def health():
        return jsonify({
            "status": "ok",
            "application": "Spendly",
            "database": "connected"
        })

    # Создание таблиц
    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5001,
        debug=app.config["DEBUG"]
    )