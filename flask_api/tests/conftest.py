import pytest
from app import create_app
from models import db
from flask_jwt_extended import create_access_token
from models.user_model import User  # Ensure correct import

@pytest.fixture(scope="session")
def app():
    """Set up a test Flask app."""
    app = create_app()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["TESTING"] = True
    app.config["JWT_SECRET_KEY"] = "test_secret_key"  # 🔥 Add this line

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope="function")
def client(app):
    """Create a new test client."""
    return app.test_client()

@pytest.fixture
def auth_token(client):
    """Registers a test user and returns a JWT token."""
    user_data = {"username": "testuser", "password": "testpassword"}

    # Register user
    reg_response = client.post("/api/auth/register", json=user_data)
    print("REGISTER RESPONSE:", reg_response.get_json())  # 🔍 Debugging

    # Log in to get token
    login_response = client.post("/api/auth/login", json=user_data)
    print("LOGIN RESPONSE:", login_response.get_json())  # 🔍 Debugging

    assert login_response.status_code == 200, f"Login failed: {login_response.get_json()}"

    token = login_response.get_json().get("access_token")
    assert token, "No access token received!"  # 🔥 Ensure token exists
    return f"Bearer {token}"
