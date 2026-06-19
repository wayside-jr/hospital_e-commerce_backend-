from models.user import User
from extensions import db, bcrypt

def register_user(full_name, email, password):
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return None, "Email already exists"

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    user = User(
        full_name=full_name,
        email=email,
        password=hashed_password
    )

    db.session.add(user)
    db.session.commit()

    return user, None


def authenticate_user(email, password):
    user = User.query.filter_by(email=email).first()

    if not user:
        return None

    if not bcrypt.check_password_hash(user.password, password):
        return None

    return user