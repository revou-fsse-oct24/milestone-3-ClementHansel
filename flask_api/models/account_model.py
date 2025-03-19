from models import db
from models.user_model import User

class Account(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    account_name = db.Column(db.String(100), nullable=False, unique=True)
    balance = db.Column(db.Numeric(10, 2), default=0.00)

    # Relationship to User model
    owner = db.relationship("User", back_populates="accounts")

    def __init__(self, owner_id, account_name, balance=0.00):
        """Initialize the Account object with the given parameters."""
        self.owner_id = owner_id
        self.account_name = account_name
        self.balance = balance

    def __repr__(self):
        return f"<Account(id={self.id}, name={self.account_name}, balance={self.balance})>"
