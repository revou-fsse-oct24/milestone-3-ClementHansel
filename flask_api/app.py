import os
from flask import Flask, jsonify
from flask_migrate import Migrate
from config import Config
from routes import register_routes
from models import db, init_db
from extensions import jwt
from flask_jwt_extended import jwt_required, get_jwt
from blacklist import blacklisted_tokens

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    Migrate(app, db)
    jwt.init_app(app)

    # Initialize the database
    init_db(app)

    # Register routes
    register_routes(app)

    # Home route
    @app.route('/')
    def home():
        return jsonify({"message": "Welcome to Hansel-Bank API"}), 200

    # Logout route
    @app.route("/logout", methods=["POST"])
    @jwt_required()
    def logout():
        jti = get_jwt().get("jti")
        if jti:
            blacklisted_tokens.add(jti)
            return jsonify({"message": "Successfully logged out"}), 200
        return jsonify({"message": "Invalid token"}), 400

    # Token blacklist check
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, jwt_payload):
        return jwt_payload.get("jti") in blacklisted_tokens

    return app

if __name__ == '__main__':
    app = create_app()
    # Run the app with debug mode controlled by environment variable
    app.run(host="0.0.0.0", port=8000, debug=os.environ.get('FLASK_DEBUG', 'false').lower() == 'true')
