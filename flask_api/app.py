from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from routes import register_routes
from models import db

def create_app():
    """Factory function to create and configure the Flask app."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    jwt = JWTManager(app)
    db.init_app(app)
    migrate = Migrate(app, db)

    # Register Blueprints (Routes)
    register_routes(app)

    @app.route('/')
    def home():
        return jsonify({"message": "Welcome to Hansel-Bank API"}), 200

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
