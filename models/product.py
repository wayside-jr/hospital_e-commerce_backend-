from extensions import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)

    # Basic info
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)

    # Pricing
    price = db.Column(db.Float, nullable=False)

    # Inventory
    stock = db.Column(db.Integer, default=0)

    # Classification
    category = db.Column(db.String(100))
    brand = db.Column(db.String(100))

    # Image
    image_url = db.Column(db.String(255))

    # Tracking
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # Relationships
    order_items = db.relationship(
        "OrderItem",
        back_populates="product"
    )