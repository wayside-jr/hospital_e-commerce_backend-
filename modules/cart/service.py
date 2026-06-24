from extensions import db
from models.cart import Cart
from models.cartItem import CartItem
from models.product import Product
from models.order import Order
from models.orderItem import OrderItem


def add_to_cart(user_id, product_id, quantity):

    user_id = int(user_id)

    product = Product.query.get(product_id)

    if not product:
        return {
            "success": False,
            "message": "Product not found"
        }

    cart = Cart.query.filter_by(
        user_id=user_id
    ).first()

    if not cart:
        cart = Cart(user_id=user_id)
        db.session.add(cart)
        db.session.flush()

    cart_item = CartItem.query.filter_by(
        cart_id=cart.id,
        product_id=product_id
    ).first()

    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(
            cart_id=cart.id,
            product_id=product_id,
            quantity=quantity
        )

        db.session.add(cart_item)

    db.session.commit()

    return {
        "success": True,
        "message": "Product added to cart"
    }

def get_cart(user_id):

    user_id = int(user_id)

    cart = Cart.query.filter_by(
        user_id=user_id
    ).first()

    if not cart:
        return {
            "items": [],
            "total": 0
        }

    items = []
    total = 0

    for item in cart.cart_items:

        subtotal = item.quantity * item.product.price

        total += subtotal

        items.append({
            "cart_item_id": item.id,
            "product_id": item.product.id,
            "product_name": item.product.name,
            "price": item.product.price,
            "quantity": item.quantity,
            "subtotal": subtotal
        })

    return {
        "items": items,
        "total": total
    }

def remove_cart_item(item_id):

    item = CartItem.query.get(item_id)

    if not item:
        return None

    db.session.delete(item)
    db.session.commit()

    return {
        "message": "Item removed from cart"
    }

def checkout(user_id):

    user_id = int(user_id)

    cart = Cart.query.filter_by(
        user_id=user_id
    ).first()

    if not cart:
        return {
            "success": False,
            "message": "Cart not found"
        }

    if not cart.cart_items:
        return {
            "success": False,
            "message": "Cart is empty"
        }

    total_amount = 0

    order = Order(
        user_id=user_id,
        status="pending"
    )

    db.session.add(order)
    db.session.flush()

    for item in cart.cart_items:

        product = item.product

        if product.stock < item.quantity:
            return {
                "success": False,
                "message": f"{product.name} is out of stock"
            }

        subtotal = product.price * item.quantity
        total_amount += subtotal

        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item.quantity,
            unit_price=product.price
        )

        db.session.add(order_item)

        product.stock -= item.quantity

    order.total_amount = total_amount

    for item in cart.cart_items:
        db.session.delete(item)

    db.session.commit()

    return {
        "success": True,
        "message": "Checkout completed successfully",
        "order_id": order.id,
        "total_amount": total_amount
    }


def checkout_cart_item(user_id, item_id):

    user_id = int(user_id)

    cart = Cart.query.filter_by(
        user_id=user_id
    ).first()

    if not cart:
        return {
            "success": False,
            "message": "Cart not found"
        }

    cart_item = CartItem.query.filter_by(
        id=item_id,
        cart_id=cart.id
    ).first()

    if not cart_item:
        return {
            "success": False,
            "message": "Cart item not found"
        }

    product = cart_item.product

    if product.stock < cart_item.quantity:
        return {
            "success": False,
            "message": f"{product.name} is out of stock"
        }

    total_amount = product.price * cart_item.quantity

    order = Order(
        user_id=user_id,
        status="pending",
        total_amount=total_amount
    )

    db.session.add(order)
    db.session.flush()

    order_item = OrderItem(
        order_id=order.id,
        product_id=product.id,
        quantity=cart_item.quantity,
        unit_price=product.price
    )

    db.session.add(order_item)

    product.stock -= cart_item.quantity

    db.session.delete(cart_item)

    db.session.commit()

    return {
        "success": True,
        "message": "Item checked out successfully",
        "order_id": order.id,
        "total_amount": total_amount
    }