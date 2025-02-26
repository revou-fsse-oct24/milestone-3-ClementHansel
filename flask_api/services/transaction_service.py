from models.transaction_model import Transaction, db
from models.account_model import Account
from datetime import datetime

def create_transaction(account_id, amount, transaction_type):
    """
    Create a new transaction and update the account balance accordingly.
    """
    account = Account.query.filter_by(id=account_id).first()
    if not account:
        return {'error': 'Account not found'}, 404

    # Validate transaction type
    if transaction_type not in ['deposit', 'withdrawal']:
        return {'error': 'Invalid transaction type'}, 400

    # Validate amount
    try:
        amount = float(amount)
        if amount <= 0:
            return {'error': 'Amount must be a positive number'}, 400
    except ValueError:
        return {'error': 'Invalid amount format'}, 400

    if transaction_type == 'withdrawal' and account.balance < amount:
        return {'error': 'Insufficient funds'}, 400

    transaction = Transaction(
        account_id=account_id,
        amount=amount,
        transaction_type=transaction_type,
        timestamp=datetime.utcnow()
    )
    db.session.add(transaction)

    # Update account balance
    if transaction_type == 'deposit':
        account.balance += amount
    elif transaction_type == 'withdrawal':
        account.balance -= amount

    try:
        db.session.commit()
        return {'message': 'Transaction successful', 'transaction_id': transaction.id}, 201
    except Exception as e:
        db.session.rollback()  # Ensure rollback on failure
        return {'error': 'Database error', 'details': str(e)}, 500

def get_transactions_by_account(account_id):
    """
    Retrieve all transactions for a given account.
    """
    transactions = Transaction.query.filter_by(account_id=account_id).all()
    return [{
        'id': t.id,
        'amount': str(t.amount),  # Ensure Numeric fields are JSON serializable
        'transaction_type': t.transaction_type,
        'timestamp': t.timestamp.isoformat()  # Convert timestamp to string
    } for t in transactions]

def get_transaction_by_id(transaction_id):
    """
    Retrieve a specific transaction by ID.
    """
    transaction = Transaction.query.filter_by(id=transaction_id).first()
    if not transaction:
        return {'error': 'Transaction not found'}, 404

    return {
        'id': transaction.id,
        'account_id': transaction.account_id,
        'amount': str(transaction.amount),  # Convert Numeric to string
        'transaction_type': transaction.transaction_type,
        'timestamp': transaction.timestamp.isoformat()  # Convert timestamp
    }
