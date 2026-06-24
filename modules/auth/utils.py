from models.user import User
from flask_jwt_extended import get_jwt_identity


def is_admin():
    user_id = int(get_jwt_identity())

    user = User.query.get(user_id)

    if not user:
        return False

    return user.role == "admin"