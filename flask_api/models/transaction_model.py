from models import db
from datetime import datetime

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id', ondelete="CASCADE"), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    transaction_type = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to Account model
    account = db.relationship("Account", backref="transactions", lazy=True)

    def __repr__(self):
        return f"<Transaction(id={self.id}, account_id={self.account_id}, type={self.transaction_type}, amount={self.amount})>"
