from extensions import db
from models.product import Product


def create_product(data):

    product = Product(
        name=data["name"],
        description=data.get("description"),
        price=data["price"],
        stock=data.get("stock", 0),
        category=data.get("category"),
        brand=data.get("brand"),
        image_url=data.get("image_url")
    )

    db.session.add(product)
    db.session.commit()

    return product


def get_products():
    return Product.query.all()


def get_product(product_id):

    return Product.query.get(product_id)


def update_product(product_id, data):

    product = Product.query.get(product_id)

    if not product:
        return None

    product.name = data.get("name", product.name)
    product.description = data.get(
        "description",
        product.description
    )
    product.price = data.get(
        "price",
        product.price
    )
    product.stock = data.get(
        "stock",
        product.stock
    )
    product.category = data.get(
        "category",
        product.category
    )
    product.brand = data.get(
        "brand",
        product.brand
    )
    product.image_url = data.get(
        "image_url",
        product.image_url
    )

    db.session.commit()

    return product


def delete_product(product_id):

    product = Product.query.get(product_id)

    if not product:
        return None

    db.session.delete(product)
    db.session.commit()

    return product