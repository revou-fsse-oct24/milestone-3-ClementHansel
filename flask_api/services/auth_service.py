from flask_jwt_extended import create_access_token
from models.user_model import User, db
from datetime import timedelta

def authenticate_user(username, password):
    """Authenticate a user and generate a JWT token if credentials are valid."""
    user = User.query.filter_by(username=username).first()
    
    if not user or not user.check_password(password):
        return None  # Explicitly return None on failure

    # Set a default expiration time (e.g., 1 hour)
    expires = timedelta(hours=1)
    
    return create_access_token(identity=str(user.id), expires_delta=expires)

def generate_token(identity, expires_hours=1):
    """Generate a JWT token with a configurable expiration time."""
    expires = timedelta(hours=expires_hours)
    return create_access_token(identity=str(identity), expires_delta=expires)
