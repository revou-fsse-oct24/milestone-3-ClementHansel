import re
import logging
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Configure logging for security events
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Secure password hashing functions
def hash_password(password):
    """Hash the given password securely."""
    try:
        return generate_password_hash(password)
    except Exception as e:
        logger.error(f"Error hashing password: {e}")
        return None  # Return None if hashing fails

def verify_password(password, hashed_password):
    """Verify the given password against the stored hash."""
    try:
        result = check_password_hash(hashed_password, password)
        if result:
            logger.info("Password verification successful")
        else:
            logger.warning("Password verification failed")
        return result
    except Exception as e:
        logger.error(f"Error verifying password: {e}")
        return False  # Always return False on failure

# Email validation function
def validate_email(email):
    """Validate email format using regex."""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$"  # ✅ Stricter validation
    return bool(re.match(pattern, email))

# Password strength validation function
def validate_password_strength(password):
    """
    Check password strength:
    - Min 8 characters
    - At least 1 uppercase letter
    - At least 1 digit
    - At least 1 special character
    """
    if len(password) < 8:
        logger.warning("Password too short")
        return False
    if not re.search(r"[A-Z]", password):
        logger.warning("Password missing uppercase letter")
        return False
    if not re.search(r"\d", password):
        logger.warning("Password missing digit")
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        logger.warning("Password missing special character")
        return False
    
    return True

# Rate limiter for login attempts (configurable)
default_limit = os.getenv("LOGIN_RATE_LIMIT", "5 per minute")  # ✅ Allows environment variable override
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[default_limit]
)
