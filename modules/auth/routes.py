from flask import Blueprint, request, jsonify

from modules.auth.service import (
    register_user,
    authenticate_user
)

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

auth_bp = Blueprint("auth", __name__)

# =========================
# 🧾 REGISTER
# =========================
@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        full_name = data.get("full_name")
        email = data.get("email")
        password = data.get("password")

        # missing fields check
        if not full_name or not email or not password:
            return jsonify({"error": "full_name, email, password are required"}), 400

        # empty string check
        if full_name.strip() == "" or email.strip() == "" or password.strip() == "":
            return jsonify({"error": "Fields cannot be empty"}), 400

        user, error = register_user(full_name, email, password)

        if error:
            return jsonify({"error": error}), 400

        return jsonify({
            "message": "User created successfully",
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email
            }
        }), 201

    except Exception as e:
        return jsonify({
            "error": "Server error during registration",
            "details": str(e)
        }), 500


# =========================
# 🔑 LOGIN
# =========================
@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "email and password are required"}), 400

        if email.strip() == "" or password.strip() == "":
            return jsonify({"error": "Fields cannot be empty"}), 400

        user = authenticate_user(email, password)

        if not user:
            return jsonify({"error": "Invalid email or password"}), 401

        access_token = create_access_token(identity=user.id)

        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email
            }
        }), 200

    except Exception as e:
        return jsonify({
            "error": "Server error during login",
            "details": str(e)
        }), 500


# =========================
# 🔒 PROTECTED ROUTE (/me)
# =========================
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    try:
        user_id = get_jwt_identity()

        if not user_id:
            return jsonify({"error": "Invalid token"}), 401

        # 🔥 FETCH USER FROM DATABASE
        from models.user import User

        user = User.query.get(user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify({
            "message": "Current user fetched successfully",
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "role": user.role
            }
        }), 200

    except Exception as e:
        return jsonify({
            "error": "Server error while fetching user",
            "details": str(e)
        }), 500