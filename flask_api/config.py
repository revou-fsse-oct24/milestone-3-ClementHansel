import os
from dotenv import load_dotenv
from datetime import timedelta
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, jwt_required, get_jwt

# Load environment variables
load_dotenv()

class Config:
    """Flask application configuration."""

    SECRET_KEY = os.getenv('SECRET_KEY', 'default_fallback_secret_key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_fallback_jwt_key')
    
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_HEADER_NAME = "Authorization"
    JWT_HEADER_TYPE = "Bearer"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 3600)))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", 86400)))

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///default.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    CORS_HEADERS = "Content-Type"
    
    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() in ["true", "1"]

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize JWT Manager
jwt = JWTManager(app)

# Store blacklisted tokens (consider using Redis for production)
blacklisted_tokens = set()

@app.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """Logout and blacklist token."""
    jti = get_jwt().get("jti")
    if jti:
        blacklisted_tokens.add(jti)
        return jsonify({"message": "Successfully logged out"}), 200
    return jsonify({"message": "Invalid token"}), 400

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    """Check if token is blacklisted."""
    return jwt_payload.get("jti") in blacklisted_tokens

# Debugging: Ensure env variables are loaded
print("Loaded JWT_SECRET_KEY:", os.getenv('JWT_SECRET_KEY'))
