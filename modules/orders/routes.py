from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from .service import (
    create_order,
    get_user_orders,
    get_order_by_id,
    get_all_orders,
    update_order_status
)

from modules.auth.utils import is_admin

orders_bp = Blueprint(
    "orders",
    __name__
)


# =========================
# CREATE ORDER
# =========================
@orders_bp.route("/", methods=["POST"])
@jwt_required()
def place_order():

    user_id = get_jwt_identity()

    data = request.get_json()

    result = create_order(
        user_id=user_id,
        items=data.get("items", [])
    )

    if not result.get("success"):
        return jsonify(result), 400

    return jsonify(result), 201


# =========================
# GET MY ORDERS
# =========================
@orders_bp.route("/", methods=["GET"])
@jwt_required()
def get_orders():

    user_id = get_jwt_identity()

    orders = get_user_orders(user_id)

    return jsonify(orders), 200


# =========================
# GET SINGLE ORDER
# =========================
@orders_bp.route("/<int:order_id>", methods=["GET"])
@jwt_required()
def get_order(order_id):

    user_id = get_jwt_identity()

    order = get_order_by_id(
        order_id,
        user_id
    )

    if not order:
        return jsonify({
            "error": "Order not found"
        }), 404

    return jsonify(order), 200


# =========================
# ADMIN - GET ALL ORDERS
# =========================
@orders_bp.route("/all", methods=["GET"])
@jwt_required()
def admin_get_orders():

    if not is_admin():
        return jsonify({
            "error": "Admin access required"
        }), 403

    orders = get_all_orders()

    return jsonify(orders), 200


# =========================
# ADMIN - UPDATE STATUS
# =========================
@orders_bp.route("/<int:order_id>/status", methods=["PATCH"])
@jwt_required()
def change_order_status(order_id):

    if not is_admin():
        return jsonify({
            "error": "Admin access required"
        }), 403

    data = request.get_json()

    status = data.get("status")

    if not status:
        return jsonify({
            "error": "Status is required"
        }), 400

    result = update_order_status(
        order_id,
        status
    )

    if not result:
        return jsonify({
            "error": "Order not found or invalid status"
        }), 404

    return jsonify(result), 200