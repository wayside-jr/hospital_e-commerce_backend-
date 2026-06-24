from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from .service import (
    add_to_cart,
    get_cart,
    remove_cart_item,
    checkout,
    checkout_cart_item
)

cart_bp = Blueprint(
    "cart",
    __name__
)

@cart_bp.route("/add", methods=["POST"])
@jwt_required()
def add_product_to_cart():

    user_id = get_jwt_identity()

    data = request.get_json()

    result = add_to_cart(
        user_id=user_id,
        product_id=data.get("product_id"),
        quantity=data.get("quantity", 1)
    )

    if not result["success"]:
        return jsonify(result), 400

    return jsonify(result), 201

@cart_bp.route("/", methods=["GET"])
@jwt_required()
def view_cart():

    user_id = get_jwt_identity()

    result = get_cart(user_id)

    return jsonify(result), 200

@cart_bp.route("/item/<int:item_id>", methods=["DELETE"])
@jwt_required()
def delete_cart_item(item_id):

    result = remove_cart_item(item_id)

    if not result:
        return jsonify({
            "error": "Item not found"
        }), 404

    return jsonify(result), 200

@cart_bp.route("/checkout", methods=["POST"])
@jwt_required()
def checkout_cart():

    user_id = get_jwt_identity()

    result = checkout(user_id)

    if not result["success"]:
        return jsonify(result), 400

    return jsonify(result), 201

@cart_bp.route("/item/<int:item_id>/checkout", methods=["POST"])
@jwt_required()
def checkout_single_item(item_id):

    user_id = get_jwt_identity()

    result = checkout_cart_item(
        user_id,
        item_id
    )

    if not result["success"]:
        return jsonify(result), 400

    return jsonify(result), 201