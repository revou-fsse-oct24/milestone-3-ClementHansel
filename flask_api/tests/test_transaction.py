import pytest
from app import create_app
from models import db

@pytest.fixture
def app():
    """Set up a test Flask app."""
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Return a test client."""
    return app.test_client()

@pytest.fixture
def auth_token(client):
    """Register and log in a test user to get a JWT token."""
    user_data = {"username": "testuser", "password": "testpassword"}
    reg_response = client.post("/api/users", json=user_data)
    assert reg_response.status_code in [200, 201, 400], f"Registration failed: {reg_response.get_json()}"
  
    login_response = client.post("/api/users/login", json=user_data)
    assert login_response.status_code == 200, f"Login failed: {login_response.get_json()}"
    token = login_response.get_json().get("access_token")
    assert token, "Failed to retrieve JWT token"
    print(f"Generated Token: {token}")
    return f"Bearer {token}"

@pytest.fixture
def test_account(client, auth_token):
    """Create a test account for the authenticated user and return account_id."""
    headers = {"Authorization": auth_token}
    account_data = {"account_name": "Test Account", "initial_balance": 1000}
    response = client.post("/api/accounts", json=account_data, headers=headers)
    assert response.status_code in [200, 201], f"Account creation failed: {response.get_json()}"
    response_data = response.get_json()
    assert response_data and "account_id" in response_data, f"Invalid account creation response: {response_data}"
    print(f"Created Account ID: {response_data.get('account_id')}")
    return response_data.get("account_id")

def test_create_transaction(client, auth_token, test_account):
    """Test transaction creation with JWT authentication and valid account."""
    headers = {"Authorization": auth_token}
    transaction_data = {
        "account_id": test_account,
        "amount": 100,
        "type": "deposit"
    }
    response = client.post("/api/transactions", json=transaction_data, headers=headers)
    print(f"Transaction Response: {response.get_json()}")
    assert response.status_code == 201, f"Unexpected status code: {response.status_code}, Response: {response.get_json()}"
