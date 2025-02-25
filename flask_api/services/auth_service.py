from flask_jwt_extended import create_access_token
from models.user_model import User, db

def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        # Ensure identity is a string
        return create_access_token(identity=str(user.id))
    return None

def generate_token(identity):
    return create_access_token(identity=str(identity))
