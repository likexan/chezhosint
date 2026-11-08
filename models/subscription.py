from datetime import datetime, timezone

from extensions import db


class Subscription(db.Model):
    __tablename__ = "subscriptions"

    id = db.Column(db.Integer, primary_key=True)

    # Основная информация
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # Стоимость
    price = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(3), nullable=False, default="EUR")

    # Периодичность
    billing_cycle = db.Column(
        db.String(20),
        nullable=False,
        default="monthly"
    )

    # Даты
    start_date = db.Column(db.Date, nullable=False)
    next_payment_date = db.Column(db.Date, nullable=False)

    # Статус
    status = db.Column(
        db.String(20),
        nullable=False,
        default="active"
    )

    # Дополнительная информация
    website_url = db.Column(db.String(500), nullable=True)

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Связи
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id"),
        nullable=True
    )

    user = db.relationship(
        "User",
        back_populates="subscriptions"
    )

    category = db.relationship(
        "Category",
        back_populates="subscriptions"
    )

    payments = db.relationship(
        "Payment",
        back_populates="subscription",
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": float(self.price),
            "currency": self.currency,
            "billing_cycle": self.billing_cycle,
            "start_date": self.start_date.isoformat(),
            "next_payment_date": self.next_payment_date.isoformat(),
            "status": self.status,
            "website_url": self.website_url,
            "category_id": self.category_id,
            "created_at": self.created_at.isoformat()
        }

    def __repr__(self):
        return f"<Subscription {self.name}>"