from models.transaction_model import Transaction, db
from models.account_model import Account
from datetime import datetime


def validate_transaction_type(transaction_type):
    """Validate the transaction type is either 'deposit' or 'withdrawal'."""
    if transaction_type not in ['deposit', 'withdrawal']:
        return False, "Invalid transaction type"
    return True, None


def validate_amount(amount):
    """Validate the amount is a positive number."""
    try:
        amount = float(amount)
        if amount <= 0:
            return False, "Amount must be a positive number"
        return True, amount
    except ValueError:
        return False, "Invalid amount format"


def create_transaction(account_id, amount, transaction_type):
    """
    Create a new transaction and update the account balance accordingly.
    """
    account = Account.query.filter_by(id=account_id).first()
    if not account:
        return {'error': 'Account not found'}, 404

    # Validate transaction type
    is_valid, error_message = validate_transaction_type(transaction_type)
    if not is_valid:
        return {'error': error_message}, 400

    # Validate amount
    is_valid, amount = validate_amount(amount)
    if not is_valid:
        return {'error': error_message}, 400

    if transaction_type == 'withdrawal' and account.balance < amount:
        return {'error': 'Insufficient funds'}, 400

    # Create the transaction
    transaction = Transaction(
        account_id=account_id,
        amount=amount,
        transaction_type=transaction_type,
        timestamp=datetime.utcnow()
    )
    db.session.add(transaction)

    # Update account balance based on transaction type
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
        'amount': str(t.amount),  # Ensure numeric fields are JSON serializable
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
        'amount': str(transaction.amount),  # Convert numeric to string
        'transaction_type': transaction.transaction_type,
        'timestamp': transaction.timestamp.isoformat()  # Convert timestamp to string
    }
