import re
from models.user_model import User, db

def register_user(username, password, email, address=None, phone=None):
    """Register a new user with validation checks."""
    if User.query.filter_by(username=username).first():
        return {"error": "Username already exists"}, 400
    if email:
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):  # Validate email format
            return {"error": "Invalid email format"}, 400
        if User.query.filter_by(email=email).first():
            return {"error": "Email already registered"}, 400

    if len(password) < 8 or not re.search(r"\d", password) or not re.search(r"[A-Z]", password):
        return {"error": "Password must be at least 8 characters long, include a number and an uppercase letter"}, 400

    new_user = User(username=username, email=email, address=address, phone=phone)
    new_user.set_password(password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return {"user_id": str(new_user.id)}, 201  # Return user ID as string
    except Exception as e:
        db.session.rollback()  # Rollback on failure
        return {"error": "Database error", "details": str(e)}, 500

def get_user_by_id(user_id):
    """Retrieve a user by their ID."""
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return {"error": "User not found"}, 404
    return {
        "user_id": str(user.id),
        "username": user.username,
        "email": user.email,
        "address": user.address,
        "phone": user.phone
    }, 200

def update_user(user_id, **kwargs):
    """Update user details with validation."""
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return {"error": "User not found"}, 404

    valid_fields = {"username", "email", "address", "phone"}  # Only allow valid fields
    for key, value in kwargs.items():
        if key in valid_fields and value is not None:
            if key == "email" and not re.match(r"[^@]+@[^@]+\.[^@]+", value):
                return {"error": "Invalid email format"}, 400
            setattr(user, key, value)

    try:
        db.session.commit()
        return {"message": "User updated successfully"}, 200
    except Exception as e:
        db.session.rollback()  # Ensure rollback on failure
        return {"error": "Database error", "details": str(e)}, 500

def delete_user(user_id):
    """Delete a user from the system."""
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return {"error": "User not found"}, 404

    try:
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully"}, 200
    except Exception as e:
        db.session.rollback()  # Rollback if error occurs
        return {"error": "Database error", "details": str(e)}, 500
