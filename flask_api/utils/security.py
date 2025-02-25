import re
import logging
from werkzeug.security import generate_password_hash, check_password_hash
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Password hashing functions
def hash_password(password):
    """Hash the given password securely."""
    return generate_password_hash(password)

def verify_password(password, hashed_password):
    """Verify the given password against the stored hash."""
    return check_password_hash(hashed_password, password)

# Email validation function
def validate_email(email):
    """Validate email format using regex."""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

# Password strength validation function
def validate_password_strength(password):
    """Check password strength: min 8 characters, at least 1 uppercase, 1 number, 1 special char."""
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):  # At least one uppercase letter
        return False
    if not re.search(r"\d", password):  # At least one digit
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):  # At least one special character
        return False
    return True

# Rate limiter for login attempts
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["5 per minute"]
)
