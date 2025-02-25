def test_unauthorized_access(client):
    """Test accessing a protected route without authentication."""
    response = client.get("/api/users/me")  # No auth token

    assert response.status_code == 401, f"Unexpected status: {response.status_code}, Response: {response.get_data(as_text=True)}"
    
    # Handle cases where response may not be JSON
    try:
        data = response.get_json() or {}
    except Exception:
        data = {}

    # Ensure a proper error message is returned
    assert "message" in data or "msg" in data, f"Unexpected error format: {data}"
    assert data.get("message", data.get("msg")) == "Missing Authorization Header", "Unexpected unauthorized access message"
