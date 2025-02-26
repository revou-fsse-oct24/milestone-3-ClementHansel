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
    user_data = {
        "username": "testuser",
        "password": "testpassword",
        "email": "testuser@example.com"
    }

    # Attempt to register a user
    reg_response = client.post("/api/users/register", json=user_data)
    
    if reg_response.status_code not in [200, 201]:
        reg_data = reg_response.get_json()
        if "User already exists" not in reg_data.get("message", ""):
            pytest.fail(f"Unexpected registration error: {reg_data}")

    # Login to get token
    login_resp = client.post("/api/users/login", json=user_data)
    assert login_resp.status_code == 200, f"Login failed: {login_resp.get_json()}"
    assert login_resp.is_json, f"Expected JSON response but got: {login_resp.data}"
    
    token = login_resp.get_json().get("access_token")
    
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
    assert response.is_json, f"Expected JSON but got: {response.data}"

    response_data = response.get_json()
    assert response_data and "account_id" in response_data, f"Invalid account creation response: {response_data}"

    return response_data.get("account_id")

def test_create_transaction(client, auth_token, test_account):
    """Test transaction creation with JWT authentication and valid account."""
    headers = {"Authorization": auth_token}
    transaction_data = {
    "account_id": test_account,
    "amount": 100,
    "transaction_type": "deposit"
    }

    response = client.post("/api/transactions", json=transaction_data, headers=headers)
    response_json = response.get_json()
    
    assert response.status_code == 201, f"Unexpected status code: {response.status_code}, Response: {response_json}"
    assert response.is_json, f"Expected JSON but got: {response.data}"
    assert "transaction_id" in response_json, "Transaction ID missing in response"
