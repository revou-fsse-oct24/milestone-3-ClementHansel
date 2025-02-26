def test_logout_user(client, auth_token):
    """Test logging out a user and ensure token is invalidated."""
    headers = {"Authorization": auth_token}

    # Perform logout
    response = client.post("/api/users/logout", headers=headers)

    assert response.status_code == 200, f"Logout failed: {response.status_code}"
    assert response.is_json, f"Expected JSON response but got: {response.data}"

    data = response.get_json() or {}
    assert "message" in data, "Logout message missing"
    assert data.get("message") == "Successfully logged out", f"Unexpected logout message: {data}"

    # Attempt to access a protected endpoint after logout
    protected_response = client.get("/api/users/profile", headers=headers)

    assert protected_response.status_code in [401, 403], f"Token should be invalid after logout, but got {protected_response.status_code}"

    print("✅ Logout test passed successfully!")  # Debug message
