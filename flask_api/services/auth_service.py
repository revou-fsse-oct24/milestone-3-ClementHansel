from flask_jwt_extended import create_access_token
from models.user import User, db

def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return create_access_token(identity=user.id)
    return None
