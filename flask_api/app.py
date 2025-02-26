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

    db.init_app(app)
    Migrate(app, db)
    jwt.init_app(app)

    init_db(app)
    with app.app_context():
        db.create_all()
    
    register_routes(app)

    @app.route('/')
    def home():
        return jsonify({"message": "Welcome to Hansel-Bank API"}), 200

    @app.route("/logout", methods=["POST"])
    @jwt_required()
    def logout():
        jti = get_jwt().get("jti")
        if jti:
            blacklisted_tokens.add(jti)
            return jsonify({"message": "Successfully logged out"}), 200
        return jsonify({"message": "Invalid token"}), 400

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in blacklisted_tokens

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
