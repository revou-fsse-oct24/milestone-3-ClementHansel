from models import db
from datetime import datetime

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id', ondelete="CASCADE"), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    transaction_type = db.Column(db.String(10), nullable=False)  # 'deposit', 'withdrawal', etc.
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to Account model
    account = db.relationship("Account", backref="transactions", lazy=True)

    def __init__(self, account_id, amount, transaction_type, timestamp=None):
        self.account_id = account_id
        self.amount = amount
        self.transaction_type = transaction_type  # Ensure you are using 'transaction_type' here
        if timestamp:
            self.timestamp = timestamp
        else:
            self.timestamp = datetime.utcnow()

    def __repr__(self):
        return f"<Transaction(id={self.id}, account_id={self.account_id}, type={self.transaction_type}, amount={self.amount})>"
