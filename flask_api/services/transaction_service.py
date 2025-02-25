from models.transaction_model import Transaction, db
from models.account_model import Account
from datetime import datetime

def create_transaction(account_id, amount, type):
    """
    Create a new transaction and update the account balance accordingly.
    """
    account = Account.query.get(account_id)
    if not account:
        return {'error': 'Account not found'}, 404

    if type not in ['deposit', 'withdrawal']:
        return {'error': 'Invalid transaction type'}, 400
    
    if type == 'withdrawal' and account.balance < amount:
        return {'error': 'Insufficient funds'}, 400
    
    transaction = Transaction(
        account_id=account_id,
        amount=amount,
        type=type,
        timestamp=datetime.utcnow()
    )
    db.session.add(transaction)
    
    # Update account balance
    if type == 'deposit':
        account.balance += amount
    elif type == 'withdrawal':
        account.balance -= amount
    
    db.session.commit()
    return {'message': 'Transaction successful', 'transaction_id': transaction.id}, 201

def get_transactions_by_account(account_id):
    """
    Retrieve all transactions for a given account.
    """
    transactions = Transaction.query.filter_by(account_id=account_id).all()
    return [{'id': t.id, 'amount': t.amount, 'type': t.type, 'timestamp': t.timestamp} for t in transactions]

def get_transaction_by_id(transaction_id):
    """
    Retrieve a specific transaction by ID.
    """
    transaction = Transaction.query.get(transaction_id)
    if not transaction:
        return {'error': 'Transaction not found'}, 404
    return {
        'id': transaction.id,
        'account_id': transaction.account_id,
        'amount': transaction.amount,
        'type': transaction.type,
        'timestamp': transaction.timestamp
    }
