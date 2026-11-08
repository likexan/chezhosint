
from pathlib import Path

from flask import Flask, jsonify, render_template

from config import Config
from extensions import db

from models import User, Subscription, Category, Payment
from routes.auth import auth_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Создаём папку instance, если её ещё нет
    Path(app.instance_path).mkdir(
        parents=True,
        exist_ok=True
    )

    # Инициализация базы данных
    db.init_app(app)

    # Подключение маршрутов авторизации
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

    # Создание таблиц базы данных
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
