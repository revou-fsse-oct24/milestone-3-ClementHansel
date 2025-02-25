def test_delete_user(client, auth_token):
    """Test deleting a user."""
    # Ensure the test user exists
    user_response = client.get("/profile", headers={"Authorization": auth_token})
    assert user_response.status_code == 200, f"User profile not found: {user_response.get_json()}"
    
    user_id = user_response.get_json().get("user_id")
    assert user_id, "User ID missing in response"

    # Delete user
    delete_response = client.delete(f"/users/{user_id}", headers={"Authorization": auth_token})
    assert delete_response.status_code == 200, f"User deletion failed: {delete_response.get_json()}"
