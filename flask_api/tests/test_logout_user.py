def test_logout_user(client, auth_token):
    """Test logging out a user and ensure token is invalidated."""
    headers = {"Authorization": auth_token}

    # Perform logout
    response = client.post("/api/users/logout", headers=headers)
    assert response.status_code == 200, f"Logout failed: {response.get_json()}"
    
    data = response.get_json() or {}
    assert "message" in data, "Logout message missing"
    assert data.get("message") == "Logout successful", f"Unexpected logout message: {data}"

    # Attempt to access a protected endpoint after logout
    protected_response = client.get("/api/users/me", headers=headers)
    assert protected_response.status_code in [401, 403], "Token should be invalid after logout"

    print("Logout test passed successfully!")  # Optional debug message
