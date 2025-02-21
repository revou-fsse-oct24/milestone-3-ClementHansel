import pytest
from app import create_app
from models import db
from flask_jwt_extended import create_access_token
from models.account_model import Account
from models.transaction_model import Transaction

@pytest.fixture
def app():
    """Set up a test Flask app."""
    app = create_app("testing")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["TESTING"] = True

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client():
    """Create a new test client and database for each test."""
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

@pytest.fixture
def auth_token(app):
    """Generates a JWT token for a test user."""
    with app.app_context():
        token = create_access_token(identity=1)
        return f"Bearer {token}"
