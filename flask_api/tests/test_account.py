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
    user_data = {"username": "accountuser", "password": "testpassword"}
    reg_resp = client.post("/api/users", json=user_data)
    login_resp = client.post("/api/users/login", json=user_data)
    token = login_resp.get_json().get("access_token")
    assert token, "Failed to get token"
    print(f"Generated Token: {token}")
    return f"Bearer {token}"

@pytest.fixture
def test_account(client, auth_token):
    """Create a test account for the authenticated user and return its account_id."""
    headers = {"Authorization": auth_token}
    account_data = {"account_name": "Test Account", "initial_balance": 1000}
    response = client.post("/api/accounts", json=account_data, headers=headers)
    assert response.status_code in [200, 201], f"Account creation failed: {response.get_json()}"
    response_data = response.get_json()
    assert response_data and "account_id" in response_data, f"Invalid account response: {response_data}"
    account_id = response_data.get("account_id")
    print(f"Created Account ID: {account_id}")
    return account_id

def test_get_specific_account(client, auth_token, test_account):
    """Test retrieving a specific account by its ID."""
    headers = {"Authorization": auth_token}
    response = client.get(f"/api/accounts/{test_account}", headers=headers)
    assert response.status_code == 200, f"Get account failed: {response.get_json()}"
    data = response.get_json()
    assert data.get("id") == test_account, "Returned account ID does not match"
    assert "account_name" in data, "Account name missing in response"

def test_update_account(client, auth_token, test_account):
    """Test updating a specific account."""
    headers = {"Authorization": auth_token}
    update_data = {"account_name": "Updated Account", "initial_balance": 1500}
    response = client.put(f"/api/accounts/{test_account}", json=update_data, headers=headers)
    assert response.status_code == 200, f"Update account failed: {response.get_json()}"
    data = response.get_json()
    assert data.get("account_name") == "Updated Account", "Account name was not updated correctly"
    assert data.get("balance") == 1500, "Account balance was not updated correctly"

def test_delete_account(client, auth_token, test_account):
    """Test deleting a specific account."""
    headers = {"Authorization": auth_token}
    response = client.delete(f"/api/accounts/{test_account}", headers=headers)
    assert response.status_code == 200, f"Delete account failed: {response.get_json()}"
    data = response.get_json()
    assert data.get("message") == "Account deleted", "Delete account message not as expected"

    response = client.get(f"/api/accounts/{test_account}", headers=headers)
    assert response.status_code == 404, "Deleted account still retrievable"
