import os
from flask import Flask, jsonify
from flask_migrate import Migrate
from config import Config
from routes import register_routes
from models import db, init_db
from extensions import jwt  # Import jwt from extensions.py
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

# Store blacklisted tokens
blacklisted_tokens = set()

def create_app():
    """Factory function to create and configure the Flask app."""
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # Initialize extensions
    jwt.init_app(app)  # Attach JWT to the app
    migrate = Migrate(app, db)

    # Initialize database
    init_db(app)
    
    with app.app_context():
        db.create_all()  # Only for development/testing

    # Register Blueprints (Routes)
    register_routes(app)

    @app.route('/')
    def home():
        return jsonify({"message": "Welcome to Hansel-Bank API"}), 200

    @app.route("/logout", methods=["POST"])
    @jwt_required()
    def logout():
        """Invalidate the token by adding it to the blacklist."""
        jti = get_jwt()["jti"]
        blacklisted_tokens.add(jti)
        return jsonify({"message": "Successfully logged out"}), 200

    # Move this function below jwt.init_app(app) to avoid errors
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, jwt_payload):
        """Check if a token is blacklisted."""
        return jwt_payload["jti"] in blacklisted_tokens

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
