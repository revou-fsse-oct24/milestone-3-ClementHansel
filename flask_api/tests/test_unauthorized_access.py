def test_unauthorized_access(client):
    """Test accessing a protected route without authentication."""
    response = client.get("/api/users/me")  # No auth token

    assert response.status_code == 401, f"Unexpected status: {response.status_code}, Response: {response.get_data(as_text=True)}"

    # Handle cases where response may not be JSON
    if response.is_json:
        data = response.get_json() or {}
    else:
        data = {}

    # Ensure a proper error message is returned
    expected_messages = ["Missing Authorization Header", "Not authenticated", "Unauthorized"]
    msg_val = data.get("message", data.get("msg", ""))
    assert any(msg in msg_val for msg in expected_messages), f"Unexpected unauthorized access message: {data}"
