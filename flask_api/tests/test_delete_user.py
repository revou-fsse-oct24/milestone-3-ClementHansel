def test_delete_user(client, auth_token):
    """Test deleting a user."""
    
    # Ensure the test user exists
    user_response = client.get("/api/users/profile", headers={"Authorization": auth_token})
    
    assert user_response.status_code == 200, f"User profile not found: {user_response.status_code}"
    assert user_response.is_json, f"Expected JSON response but got: {user_response.data}"

    user_data = user_response.get_json()
    user_id = user_data.get("user_id")
    assert user_id, "User ID missing in response"

    # Delete the user
    delete_response = client.delete(f"/api/users/{user_id}", headers={"Authorization": auth_token})
    
    assert delete_response.status_code == 200, f"User deletion failed: {delete_response.get_json()}"
    assert delete_response.is_json, f"Expected JSON response but got: {delete_response.data}"

    data = delete_response.get_json()
    assert data.get("message") == "User deleted successfully", f"Unexpected delete response: {data}"

    # Confirm user is actually deleted
    confirm_delete = client.get("/api/users/profile", headers={"Authorization": auth_token})
    assert confirm_delete.status_code in [401, 403, 404], "User still accessible after deletion"
