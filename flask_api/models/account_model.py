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

    def __repr__(self):
        return f"<Account(id={self.id}, name={self.account_name}, balance={self.balance})>"
