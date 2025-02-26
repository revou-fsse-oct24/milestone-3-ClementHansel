import os
import pytest
from app import create_app, db

@pytest.fixture
def app():
    """Set up a test Flask app with a fresh database."""
    # Set test-specific environment variables before creating the app
    os.environ["DATABASE_URL"] = "sqlite:///:memory:"  # Use in-memory database for tests
    os.environ["FLASK_DEBUG"] = "True"
    os.environ["TESTING"] = "True"
    
    # Now create the app
    app = create_app()
    app.config["TESTING"] = True

    with app.app_context():
        db.drop_all()  # Ensure a fresh start
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()  # Cleanup after tests

@pytest.fixture
def client(app):
    """Return a test client."""
    return app.test_client()

@pytest.fixture
def auth_token(client):
    """Register and log in a test user to get a JWT token."""
    user_data = {
    "username": "accountuser",
    "password": "testpassword",
    "email": "accountuser@example.com"
}


    # Register user if needed
    reg_resp = client.post("/api/users/register", json=user_data)
    if reg_resp.status_code not in [200, 201]:
        print(f"User registration skipped: {reg_resp.get_json()}")

    # Login to get token
    login_resp = client.post("/api/users/login", json=user_data)
    assert login_resp.status_code == 200, f"Login failed: {login_resp.get_json()}"
    assert login_resp.is_json, f"Expected JSON response but got: {login_resp.data}"

    token = login_resp.get_json().get("access_token")
    assert token, "Failed to retrieve JWT token"
    print(f"Generated Token: {token}")

    return f"Bearer {token}"
