from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

def init_db(app):
    """Initialize the database with the Flask app."""
    # Ensure that SQLAlchemy is only initialized once for the app
    if not hasattr(app, 'extensions') or 'sqlalchemy' not in app.extensions:
        db.init_app(app)
        print("Database initialized successfully.")
    else:
        print("Database already initialized.")

# Import models to register them with SQLAlchemy
from models.user_model import User
from models.account_model import Account
from models.transaction_model import Transaction
from models.token_blacklist import TokenBlacklist
