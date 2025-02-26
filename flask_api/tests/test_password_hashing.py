from models.user_model import User

def test_password_hashing(client, auth_token):
    """Test that passwords are properly hashed in the database."""
    
    headers = {"Authorization": auth_token}

    # Fetch user profile to get the username
    response = client.get("/api/users/profile", headers=headers)
    
    assert response.status_code == 200, f"Failed to get user profile: {response.status_code}"
    assert response.is_json, f"Expected JSON but got: {response.data}"

    user_data = response.get_json()
    username = user_data.get("username")
    assert username, "Username not found in user profile"

    # Ensure correct application context
    with client.application.app_context():
        user = User.query.filter_by(username=username).first()
        
        assert user, f"User with username '{username}' not found in the database"
        assert hasattr(user, "password_hash"), "User model does not have a password_hash attribute"
        
        # Ensure password is properly hashed and not stored in plaintext
        assert user.password_hash != "testpassword", "Password is stored in plaintext"

    print("✅ Password hashing test passed successfully!")  # Debug message
