from flask import Flask
from dotenv import load_dotenv
import os

from extensions import db, migrate

load_dotenv()

app = Flask(__name__)

# CONFIG
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# INIT DB
db.init_app(app)
migrate.init_app(app, db)

# IMPORT MODELS (important for migrations)
from models.user import User

# IMPORT BLUEPRINT
from modules.auth.routes import auth_bp
app.register_blueprint(auth_bp, url_prefix="/auth")

@app.route("/")
def home():
    return {"message": "API running with Supabase"}

if __name__ == "__main__":
    app.run(debug=True)