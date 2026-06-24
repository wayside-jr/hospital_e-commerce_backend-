from flask import Flask
from dotenv import load_dotenv
import os

from extensions import db, migrate
from flask_jwt_extended import JWTManager

load_dotenv()

# INIT JWT
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    # ======================
    # CONFIG
    # ======================
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    # JWT config (NEW)
    app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY")

    # ======================
    # INIT EXTENSIONS
    # ======================
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # ======================
    # IMPORT MODELS (MIGRATIONS)
    # ======================
    import models

    # ======================
    # REGISTER BLUEPRINTS
    # ======================
    from modules.auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from modules.products.routes import product_bp
    app.register_blueprint(product_bp , url_prefix ="/products")

    from modules.orders.routes import orders_bp
    app.register_blueprint(orders_bp , url_prefix = "/orders")

    from modules.cart.routes import cart_bp
    app.register_blueprint(cart_bp   ,url_prefix = "/cart") 

    # ======================
    # BASE ROUTE
    # ======================
    @app.route("/")
    def home():
        return {"message": "API running with Supabase"}

    return app


# RUN APP
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)