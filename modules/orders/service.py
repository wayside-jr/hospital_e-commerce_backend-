from extensions import db
from models.order import Order
from models.orderItem import OrderItem
from models.product import Product


# =========================
# CREATE ORDER
# =========================
def create_order(user_id, items):

    user_id = int(user_id)

    if not items:
        return {
            "success": False,
            "message": "Order must contain at least one item"
        }

    total_amount = 0

    order = Order(
        user_id=user_id,
        status="pending"
    )

    db.session.add(order)
    db.session.flush()

    for item in items:

        product = Product.query.get(
            item["product_id"]
        )

        if not product:
            return {
                "success": False,
                "message": "Product not found"
            }

        quantity = item["quantity"]

        if quantity <= 0:
            return {
                "success": False,
                "message": "Quantity must be greater than zero"
            }

        if product.stock < quantity:
            return {
                "success": False,
                "message": f"{product.name} is out of stock"
            }

        subtotal = product.price * quantity
        total_amount += subtotal

        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=quantity,
            unit_price=product.price
        )

        db.session.add(order_item)

        # Reduce stock
        product.stock -= quantity

    order.total_amount = total_amount

    db.session.commit()

    return {
        "success": True,
        "message": "Order created successfully",
        "order_id": order.id,
        "total_amount": total_amount
    }


# =========================
# GET USER ORDERS
# =========================
def get_user_orders(user_id):

    orders = Order.query.filter_by(
        user_id=int(user_id)
    ).all()

    results = []

    for order in orders:

        results.append({
            "id": order.id,
            "total_amount": order.total_amount,
            "status": order.status,
            "created_at": order.created_at
        })

    return results


# =========================
# GET SINGLE ORDER
# =========================
def get_order_by_id(order_id, user_id):

    order = Order.query.filter_by(
        id=order_id,
        user_id=int(user_id)
    ).first()

    if not order:
        return None

    items = []

    for item in order.order_items:

        items.append({
            "product_id": item.product.id,
            "product_name": item.product.name,
            "quantity": item.quantity,
            "unit_price": item.unit_price
        })

    return {
        "id": order.id,
        "total_amount": order.total_amount,
        "status": order.status,
        "created_at": order.created_at,
        "items": items
    }


# =========================
# ADMIN - GET ALL ORDERS
# =========================
def get_all_orders():

    orders = Order.query.all()

    results = []

    for order in orders:

        results.append({
            "id": order.id,
            "user_id": order.user_id,
            "customer_name": order.user.full_name,
            "customer_email": order.user.email,
            "total_amount": order.total_amount,
            "status": order.status,
            "created_at": order.created_at
        })

    return results


# =========================
# ADMIN - UPDATE STATUS
# =========================
def update_order_status(order_id, status):

    allowed_statuses = [
        "pending",
        "processing",
        "shipped",
        "delivered",
        "cancelled"
    ]

    if status not in allowed_statuses:
        return None

    order = Order.query.get(order_id)

    if not order:
        return None

    order.status = status

    db.session.commit()

    return {
        "message": "Order status updated successfully",
        "order_id": order.id,
        "status": order.status
    }