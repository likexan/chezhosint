from extensions import db


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(80),
        nullable=False
    )

    # Цвет категории для интерфейса
    color = db.Column(
        db.String(7),
        nullable=False,
        default="#808080"
    )

    # Иконка категории
    icon = db.Column(
        db.String(50),
        nullable=False,
        default="📦"
    )

    # Пользовательская или системная категория
    is_default = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True,
        index=True
    )

    subscriptions = db.relationship(
        "Subscription",
        back_populates="category"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color,
            "icon": self.icon,
            "is_default": self.is_default,
            "user_id": self.user_id
        }

    def __repr__(self):
        return f"<Category {self.name}>"