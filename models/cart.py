from extensions import db

class Cart(db.Model):
    __tablename__ = "carts"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    user = db.relationship(
        "User",
        back_populates="cart"
    )

    cart_items = db.relationship(
        "CartItem",
        back_populates="cart",
        cascade="all, delete-orphan"
    )