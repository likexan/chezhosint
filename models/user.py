from datetime import datetime, timezone

from extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    # Telegram
    telegram_id = db.Column(
        db.BigInteger,
        unique=True,
        nullable=False,
        index=True
    )

    username = db.Column(db.String(64), nullable=True)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=True)

    # Настройки
    currency = db.Column(db.String(3), default="EUR", nullable=False)

    notifications_enabled = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    # Дата регистрации
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Связи
    subscriptions = db.relationship(
        "Subscription",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    payments = db.relationship(
        "Payment",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "telegram_id": self.telegram_id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "currency": self.currency,
            "notifications_enabled": self.notifications_enabled,
            "created_at": self.created_at.isoformat()
        }

    def __repr__(self):
        return f"<User {self.telegram_id}>"