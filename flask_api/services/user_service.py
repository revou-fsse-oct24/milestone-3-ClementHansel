from models.user_model import User, db

def register_user(username, password, email, address=None, phone=None):
    if User.query.filter_by(username=username).first():
        return {"error": "Username already exists"}  # Clearer error response
    if email and User.query.filter_by(email=email).first():
        return {"error": "Email already registered"}
    
    new_user = User(username=username, email=email, address=address, phone=phone)
    new_user.set_password(password)
    
    db.session.add(new_user)
    db.session.commit()
    
    return {"user_id": str(new_user.id)}  # Return user ID as string

def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if not user:
        return {"error": "User not found"}
    return user

def update_user(user_id, **kwargs):
    user = User.query.get(user_id)
    if not user:
        return {"error": "User not found"}
    
    for key, value in kwargs.items():
        if hasattr(user, key) and value is not None:
            setattr(user, key, value)
    
    db.session.commit()
    return {"message": "User updated successfully"}

def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return {"error": "User not found"}
    
    db.session.delete(user)
    db.session.commit()
    return {"message": "User deleted successfully"}
