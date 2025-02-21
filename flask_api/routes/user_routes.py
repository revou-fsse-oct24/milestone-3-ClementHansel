from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from models import db
from models.user_model import User

user_bp = Blueprint('user_bp', __name__, url_prefix='/users')

@user_bp.route('', methods=['POST'])
def create_user():
    data = request.get_json()
    
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "User already exists"}), 400

    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"user_id": user.id}), 201

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=str(user.id))  # Ensure "sub" is a string
    return jsonify({"access_token": access_token}), 200

@user_bp.route('/me', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404
   
    return jsonify({
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
        "address": user.address,
        "phone": user.phone
    }), 200

@user_bp.route('/me', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    if "username" in data:
        user.username = data["username"]

    db.session.commit()
    return jsonify({"message": "Profile updated"}), 200

@user_bp.route('/password', methods=['PUT'])
@jwt_required()
def change_password():
    """
    Change the user's password.
    Request Body:
    {
        "old_password": "oldpass",
        "new_password": "newpass"
    }
    """
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    old_password = data.get("old_password")
    new_password = data.get("new_password")
    if not old_password or not new_password:
        return jsonify({"error": "Both old and new passwords are required"}), 400

    if not user.check_password(old_password):
        return jsonify({"error": "Old password is incorrect"}), 400

    user.set_password(new_password)
    db.session.commit()
    return jsonify({"message": "Password updated successfully"}), 200

@user_bp.route('/email', methods=['PUT'])
@jwt_required()
def change_email():
    """
    Change the user's email address.
    Request Body:
    {
        "new_email": "newemail@example.com"
    }
    Note: The User model must have an 'email' field.
    """
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    new_email = data.get("new_email")
    if not new_email:
        return jsonify({"error": "New email is required"}), 400

    if User.query.filter_by(email=new_email).first():
        return jsonify({"error": "Email already in use"}), 400

    user.email = new_email
    db.session.commit()
    return jsonify({"message": "Email updated successfully"}), 200

@user_bp.route('/profile/details', methods=['PATCH'])
@jwt_required()
def update_profile_details():
    """
    Update additional profile details such as address and phone number.
    Request Body:
    {
        "address": "123 Main St",
        "phone": "555-1234"
    }
    Note: The User model must have 'address' and 'phone' fields.
    """
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    if "address" in data:
        user.address = data["address"]
    if "phone" in data:
        user.phone = data["phone"]

    db.session.commit()
    return jsonify({"message": "Profile details updated successfully"}), 200
