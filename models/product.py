from extensions import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)

    # 🏷️ Basic info
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)

    # 💰 Pricing
    price = db.Column(db.Float, nullable=False)

    # 📦 Inventory
    stock = db.Column(db.Integer, default=0)

    # 🏷️ Classification (VERY important for catalog)
    category = db.Column(db.String(100), nullable=True)

    # 🏭 Optional catalog fields (useful for your mum)
    brand = db.Column(db.String(100), nullable=True)

    # 🖼️ Product image (URL from frontend or storage later)
    image_url = db.Column(db.String(255), nullable=True)

    # ⏱️ Tracking
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )