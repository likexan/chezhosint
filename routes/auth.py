from flask import Blueprint, jsonify, request

from config import Config
from extensions import db
from models import User
from services.telegram_auth import validate_telegram_init_data


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/api/auth/telegram", methods=["POST"])
def telegram_auth():
    # Получаем данные от frontend
    data = request.get_json(silent=True) or {}
    init_data = data.get("initData")

    if not init_data:
        return jsonify({
            "success": False,
            "error": "Telegram initData не передан"
        }), 400

    if not Config.BOT_TOKEN:
        return jsonify({
            "success": False,
            "error": "Авторизация временно недоступна"
        }), 500

    # Проверяем подлинность данных Telegram
    telegram_user = validate_telegram_init_data(
        init_data,
        Config.BOT_TOKEN
    )

    if not telegram_user:
        return jsonify({
            "success": False,
            "error": "Недействительные данные Telegram"
        }), 401

    try:
        telegram_id = int(telegram_user["id"])

        user = User.query.filter_by(
            telegram_id=telegram_id
        ).first()

        if user is None:
            # Регистрируем нового пользователя
            user = User(
                telegram_id=telegram_id,
                username=telegram_user.get("username"),
                first_name=telegram_user["first_name"],
                last_name=telegram_user.get("last_name")
            )

            db.session.add(user)

        else:
            # Обновляем существующий профиль
            user.username = telegram_user.get("username")
            user.first_name = telegram_user["first_name"]
            user.last_name = telegram_user.get("last_name")

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Авторизация успешна",
            "user": user.to_dict()
        }), 200

    except (ValueError, TypeError):
        db.session.rollback()

        return jsonify({
            "success": False,
            "error": "Некорректные данные пользователя"
        }), 400

    except Exception:
        db.session.rollback()

        return jsonify({
            "success": False,
            "error": "Ошибка сервера при авторизации"
        }), 500