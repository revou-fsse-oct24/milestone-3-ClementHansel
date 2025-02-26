def test_get_user_profile(client, auth_token):
    """Test retrieving user profile after login."""
    headers = {"Authorization": auth_token}

    # Ensure user exists before fetching profile
    user_check_response = client.get("/api/users/profile", headers=headers)
    
    assert user_check_response.status_code == 200, f"User profile not found: {user_check_response.status_code}"
    assert user_check_response.is_json, f"Expected JSON response but got: {user_check_response.data}"

    data = user_check_response.get_json() or {}

    # Validate expected response fields
    assert "username" in data, "Username missing in response"
    assert "user_id" in data, "User ID missing in response"
    assert "email" in data, "Email missing in response (expected None if not set)"
    
    print(f"User Profile Data: {data}")  # Debug info
