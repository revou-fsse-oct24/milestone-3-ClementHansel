from .user_routes import user_bp
from .account_routes import account_bp
from .transaction_routes import transaction_bp
from .auth_routes import auth_bp

def register_routes(app):
    """Register all route blueprints to the Flask app."""
    # Auth routes for authentication (login, signup, etc.)
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    # User routes for user profile, password change, etc.
    app.register_blueprint(user_bp, url_prefix='/api/users')
    
    # Account routes for account management
    app.register_blueprint(account_bp, url_prefix='/api/accounts')
    
    # Transaction routes for handling transactions
    app.register_blueprint(transaction_bp, url_prefix='/api/transactions')
