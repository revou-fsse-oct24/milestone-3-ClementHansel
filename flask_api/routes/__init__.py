from flask import Flask
from .user_routes import user_bp
from .account_routes import account_bp
from .transaction_routes import transaction_bp

def register_routes(app):
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(account_bp, url_prefix='/api/accounts')
    app.register_blueprint(transaction_bp, url_prefix='/api/transactions')
