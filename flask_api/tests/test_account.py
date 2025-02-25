import pytest
from app import create_app
from models import db

@pytest.fixture
def app():
    """Set up a test Flask app with a fresh database."""
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.drop_all()  # Ensure fresh start
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
    user_data = {"username": "accountuser", "password": "testpassword"}

    # Register user only if needed
    reg_resp = client.post("/register", json=user_data)
    if reg_resp.status_code not in [200, 201]:
        print(f"User registration skipped: {reg_resp.get_json()}")

    # Login to get token
    login_resp = client.post("/login", json=user_data)
    assert login_resp.status_code == 200, f"Login failed: {login_resp.get_json()}"
    
    token = login_resp.get_json().get("access_token")
    assert token, "Failed to get token"
    print(f"Generated Token: {token}")

    return f"Bearer {token}"

@pytest.fixture
def test_account(client, auth_token):
    """Create a test account for the authenticated user and return its account_id."""
    headers = {"Authorization": auth_token}
    
    # Ensure no pre-existing accounts for this test
    account_data = {"account_name": "Test Account", "initial_balance": 1000}
    response = client.post("/api/accounts", json=account_data, headers=headers)
    
    assert response.status_code in [200, 201], f"Account creation failed: {response.get_json()}"
    
    response_data = response.get_json()
    assert "account_id" in response_data, f"Invalid account response: {response_data}"
    
    account_id = response_data.get("account_id")
    print(f"Created Account ID: {account_id}")

    return account_id

def test_get_specific_account(client, auth_token, test_account):
    """Test retrieving a specific account by its ID."""
    headers = {"Authorization": auth_token}
    response = client.get(f"/api/accounts/{test_account}", headers=headers)
    
    assert response.status_code == 200, f"Get account failed: {response.get_json()}"
    
    data = response.get_json()
    assert data.get("id") == test_account, f"Returned account ID does not match: {data}"
    assert "account_name" in data, "Account name missing in response"

def test_update_account(client, auth_token, test_account):
    """Test updating a specific account."""
    headers = {"Authorization": auth_token}

    # Ensure the account exists before updating
    response = client.get(f"/api/accounts/{test_account}", headers=headers)
    assert response.status_code == 200, f"Account not found: {response.get_json()}"

    update_data = {"account_name": "Updated Account", "initial_balance": 1500}
    response = client.put(f"/api/accounts/{test_account}", json=update_data, headers=headers)
    
    assert response.status_code == 200, f"Update account failed: {response.get_json()}"
    data = response.get_json()
    
    assert data.get("account_name") == "Updated Account", f"Account name was not updated correctly: {data}"
    assert data.get("initial_balance") == 1500, f"Account balance was not updated correctly: {data}"

def test_delete_account(client, auth_token, test_account):
    """Test deleting a specific account."""
    headers = {"Authorization": auth_token}

    # Ensure the account exists before deleting
    response = client.get(f"/api/accounts/{test_account}", headers=headers)
    assert response.status_code == 200, f"Account not found: {response.get_json()}"

    response = client.delete(f"/api/accounts/{test_account}", headers=headers)
    
    assert response.status_code == 200, f"Delete account failed: {response.get_json()}"
    data = response.get_json()
    
    assert data.get("message") == "Account deleted", f"Delete account message not as expected: {data}"

    # Ensure the account is deleted
    response = client.get(f"/api/accounts/{test_account}", headers=headers)
    assert response.status_code == 404, "Deleted account still retrievable"
