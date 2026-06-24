from extensions import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        default="user"
    )

    # Relationships
    orders = db.relationship(
        "Order",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    cart = db.relationship(
    "Cart",
    back_populates="user",
    uselist=False,
    cascade="all, delete-orphan"
)