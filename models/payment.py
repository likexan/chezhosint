from datetime import datetime, timezone

from extensions import db


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)

    # Сумма платежа
    amount = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    currency = db.Column(
        db.String(3),
        nullable=False,
        default="EUR"
    )

    # Дата платежа
    payment_date = db.Column(
        db.Date,
        nullable=False
    )

    # Статус платежа
    status = db.Column(
        db.String(20),
        nullable=False,
        default="completed"
    )

    # Дополнительная информация
    description = db.Column(db.Text, nullable=True)

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Пользователь
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    # Подписка
    subscription_id = db.Column(
        db.Integer,
        db.ForeignKey("subscriptions.id"),
        nullable=True,
        index=True
    )

    user = db.relationship(
        "User",
        back_populates="payments"
    )

    subscription = db.relationship(
        "Subscription",
        back_populates="payments"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "amount": float(self.amount),
            "currency": self.currency,
            "payment_date": self.payment_date.isoformat(),
            "status": self.status,
            "description": self.description,
            "user_id": self.user_id,
            "subscription_id": self.subscription_id,
            "created_at": self.created_at.isoformat()
        }

    def __repr__(self):
        return f"<Payment {self.amount} {self.currency}>"