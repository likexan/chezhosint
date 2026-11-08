
import hashlib
import hmac
import json
import time

from urllib.parse import parse_qsl


def validate_telegram_init_data(init_data: str, bot_token: str):
    """
    Проверяет подлинность Telegram WebApp initData.

    Возвращает данные пользователя при успешной проверке.
    Возвращает None, если данные недействительны.
    """

    if not init_data or not bot_token:
        return None

    try:
        parsed_data = dict(
            parse_qsl(init_data, keep_blank_values=True)
        )

        received_hash = parsed_data.pop("hash", None)

        if not received_hash:
            return None

        # Формируем строку для проверки подписи
        data_check_string = "\n".join(
            f"{key}={value}"
            for key, value in sorted(parsed_data.items())
        )

        # Получаем секретный ключ Telegram WebApp
        secret_key = hmac.new(
            key=b"WebAppData",
            msg=bot_token.encode(),
            digestmod=hashlib.sha256
        ).digest()

        # Вычисляем ожидаемую подпись
        calculated_hash = hmac.new(
            key=secret_key,
            msg=data_check_string.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()

        # Сравниваем подписи
        if not hmac.compare_digest(
            calculated_hash,
            received_hash
        ):
            return None

        # Проверяем время создания данных
        auth_date = int(parsed_data.get("auth_date", 0))

        current_time = int(time.time())

        if auth_date <= 0:
            return None

        # Не принимаем данные старше 24 часов
        if current_time - auth_date > 86400:
            return None

        # Не принимаем данные из будущего
        if auth_date > current_time + 30:
            return None

        # Получаем информацию о пользователе
        user_data = json.loads(parsed_data.get("user", "{}"))

        if not user_data.get("id") or not user_data.get("first_name"):
            return None

        return user_data

    except (ValueError, TypeError, json.JSONDecodeError):
        return None
