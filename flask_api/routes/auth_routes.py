from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    jwt_required, get_jwt, create_access_token, get_jwt_identity
)
from extensions import jwt  # JWTManager instance from extensions.py
from models import db
from models.user_model import User
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

# Global blacklisted tokens set (use Redis or DB in production)
blacklisted_tokens = set()

@auth_bp.route("/register", methods=["POST"])
def register():
    """Register a new user."""
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "User already exists"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    """Login user and return a JWT token."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    user = User.query.filter_by(username=username).first()
    
    if user and check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=str(user.id))  # Ensure identity is a string
        return jsonify({'access_token': access_token, 'user_id': user.id}), 200  # Include user_id for debugging

    return jsonify({'message': 'Invalid credentials'}), 401

@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    """Get user profile."""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify({"user_id": user.id, "username": user.username}), 200

@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """Logout user and blacklist token."""
    jti = get_jwt().get("jti")  # Get JWT token identifier
    if jti:
        blacklisted_tokens.add(jti)  # Add token identifier to the blacklist
        return jsonify({"message": "Successfully logged out"}), 200
    return jsonify({"message": "Invalid token"}), 400

@auth_bp.route("/users/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    """Delete a user."""
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    
    return jsonify({"message": "User deleted successfully"}), 200

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    """Check if a token is blacklisted."""
    return jwt_payload.get("jti") in blacklisted_tokens
