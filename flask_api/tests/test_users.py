import unittest
from app import create_app
from models import db

class UserTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test app and database before each test."""
        self.app = create_app()
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up database after each test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_user(self):
        """Test user creation endpoint."""
        response = self.client.post("/api/users", json={
            "username": "test",
            "password": "1234"
        })
        
        self.assertEqual(response.status_code, 201, response.get_json())

if __name__ == '__main__':
    unittest.main()
