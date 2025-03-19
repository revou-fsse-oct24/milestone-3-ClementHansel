from flask_jwt_extended import create_access_token
from models.user_model import User, db
from datetime import timedelta
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def authenticate_user(username, password, expires_hours=1):
    """Authenticate a user and generate a JWT token if credentials are valid."""
    user = User.query.filter_by(username=username).first()

    if not user:
        logger.warning(f"Authentication failed: User '{username}' not found.")
        return {"error": "Invalid credentials"}, 401  # Return error response with 401 Unauthorized

    if not user.check_password(password):
        logger.warning(f"Authentication failed: Incorrect password for user '{username}'.")
        return {"error": "Invalid credentials"}, 401  # Return error response with 401 Unauthorized

    # Set expiration time for the token
    expires = timedelta(hours=expires_hours)
    
    try:
        # Create the access token with a specific expiration
        token = create_access_token(identity=str(user.id), expires_delta=expires)
        logger.info(f"User '{username}' authenticated successfully.")
        return {"access_token": token}, 200  # Return token and success status
    except Exception as e:
        logger.error(f"Error generating token for user '{username}': {str(e)}")
        return {"error": "Internal server error", "details": str(e)}, 500  # Handle any issues creating the token

def generate_token(identity, expires_hours=1):
    """Generate a JWT token with a configurable expiration time."""
    expires = timedelta(hours=expires_hours)
    
    try:
        # Generate access token
        token = create_access_token(identity=str(identity), expires_delta=expires)
        return token  # Return the token directly
    except Exception as e:
        logger.error(f"Error generating token for identity '{identity}': {str(e)}")
        return None  # Return None if token generation fails
