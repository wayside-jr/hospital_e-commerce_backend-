from flask import Blueprint, request, jsonify
import time

from .service import (
    create_product,
    get_products,
    get_product,
    update_product,
    delete_product
)

from sqlalchemy.exc import SQLAlchemyError


product_bp = Blueprint(
    "product",
    __name__
)


# ---------------- CREATE PRODUCT ----------------

@product_bp.route("/", methods=["POST"])
def create():

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "Request body is required"
            }), 400


        required_fields = [
            "name",
            "price"
        ]

        for field in required_fields:
            if field not in data:
                return jsonify({
                    "error": f"{field} is required"
                }), 400


        product = create_product(data)


        return jsonify({
            "message": "Product created successfully",
            "product": {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "stock": product.stock
            }
        }), 201


    except SQLAlchemyError:
        return jsonify({
            "error": "Database error occurred"
        }), 500


    except Exception:
        return jsonify({
            "error": "Something went wrong"
        }), 500






# ---------------- GET ALL PRODUCTS ----------------

@product_bp.route("/", methods=["GET"])
def get_all():

    # Start timing the entire Flask route
    request_start = time.perf_counter()

    try:
        # 1. Measure how long fetching products takes
        db_start = time.perf_counter()

        products = get_products()

        db_end = time.perf_counter()

        # 2. Measure JSON data preparation
        serialize_start = time.perf_counter()

        products_data = [
            {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "stock": product.stock,
                "category": product.category,
                "brand": product.brand,
                "image_url": product.image_url
            }
            for product in products
        ]

        serialize_end = time.perf_counter()

        # 3. Calculate the time taken in milliseconds
        db_time = (db_end - db_start) * 1000

        serialize_time = (
            serialize_end - serialize_start
        ) * 1000

        total_time = (
            serialize_end - request_start
        ) * 1000

        # 4. Print results in the Flask/Render logs
        print(
            f"PRODUCT TIMING | "
            f"DB fetch: {db_time:.2f} ms | "
            f"JSON preparation: {serialize_time:.2f} ms | "
            f"Route total: {total_time:.2f} ms | "
            f"Products: {len(products)}"
        )

        return jsonify(products_data), 200

    except Exception as e:
        print("GET PRODUCTS ERROR:", repr(e))

        return jsonify({
            "error": "Unable to fetch products"
        }), 500




# ---------------- GET ONE PRODUCT ----------------

@product_bp.route("/<int:id>", methods=["GET"])
def get_one(id):

    try:

        product = get_product(id)


        if not product:
            return jsonify({
                "error": "Product not found",
                "product_id": id
            }), 404



        return jsonify({
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "stock": product.stock,
            "category": product.category,
            "brand": product.brand,
            "image_url": product.image_url
        }), 200


    except Exception:
        return jsonify({
            "error": "Unable to fetch product"
        }), 500






# ---------------- UPDATE PRODUCT ----------------

@product_bp.route("/<int:id>", methods=["PUT"])
def update(id):

    try:

        data = request.get_json()


        if not data:
            return jsonify({
                "error": "Update data required"
            }), 400



        product = update_product(id, data)



        if not product:
            return jsonify({
                "error": "Product not found",
                "product_id": id
            }), 404



        return jsonify({
            "message": "Product updated successfully",
            "id": product.id
        }), 200



    except Exception:
        return jsonify({
            "error": "Unable to update product"
        }), 500






# ---------------- DELETE PRODUCT ----------------

@product_bp.route("/<int:id>", methods=["DELETE"])
def delete(id):

    try:

        product = delete_product(id)


        if not product:
            return jsonify({
                "error": "Product not found",
                "product_id": id
            }), 404



        return jsonify({
            "message": "Product deleted successfully",
            "id": id
        }), 200



    except ValueError as e:
        return jsonify({
            "error": str(e)
        }), 409

    except Exception as e:
        print("DELETE PRODUCT ERROR:", repr(e))
        return jsonify({
            "error": "Unable to delete product"
        }), 500
