from flask import Flask
from dotenv import load_dotenv
import os

from extensions import db, migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

load_dotenv()

# INIT JWT
# INIT JWT
jwt = JWTManager()


@jwt.invalid_token_loader
def invalid_token_callback(error):
    print("JWT ERROR:", error)
    return {
        "msg": error
    }, 422

def create_app():
    app = Flask(__name__)

# ======================
# CONFIG
# ======================
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": True,
        "pool_recycle": 1800,
        "pool_size": 5,
        "max_overflow": 10,
    }

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY")

    # ======================
    # CORS
    # ======================
    CORS(
        app,
        resources={
            r"/*": {
                "origins": [
                    "http://localhost:5173",
                    "http://127.0.0.1:5173",
                    "https://jeremy-enterprises-9nxb.onrender.com"
                ]
            }
        }
    )

    # ======================
    # INIT EXTENSIONS
    # ======================
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # ======================
    # IMPORT MODELS
    # ======================
    import models

    # ======================
    # REGISTER BLUEPRINTS
    # ======================
    from modules.auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from modules.products.routes import product_bp
    app.register_blueprint(product_bp, url_prefix="/products")

    from modules.orders.routes import orders_bp
    app.register_blueprint(orders_bp, url_prefix="/orders")

    from modules.cart.routes import cart_bp
    app.register_blueprint(cart_bp, url_prefix="/cart")

    # ======================
    # BASE ROUTE
    # ======================
    @app.route("/")
    def home():
        return {"message": "API running with Supabase"}

    return app


app = create_app() 
if __name__ == "__main__": app.run(debug=True)
