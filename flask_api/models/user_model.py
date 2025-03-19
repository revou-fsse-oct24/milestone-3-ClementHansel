from werkzeug.security import generate_password_hash, check_password_hash
from models import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)  # Increased length to 128 characters
    password_hash = db.Column(db.String(256), nullable=False)  # Increased length to 256 characters to accommodate hash
    email = db.Column(db.String(256), unique=True, nullable=True)  # Increased length to 256 characters for email
    address = db.Column(db.String(300), nullable=True)  # Increased length to 300 characters for address
    phone = db.Column(db.String(20), unique=True, nullable=True)  # Ensure phone numbers are unique

    # Relationships
    accounts = db.relationship("Account", back_populates="owner")

    def set_password(self, password):
        """Hashes and sets the user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"
