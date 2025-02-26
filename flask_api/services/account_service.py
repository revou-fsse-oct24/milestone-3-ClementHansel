from models import db
from models.account_model import Account

def create_account(owner_id, account_name=None, initial_balance=0.0):
    """Create a new account for a user, ensuring account name uniqueness."""
    if Account.query.filter_by(owner_id=owner_id, account_name=account_name).first():
        return None  # Prevent duplicate account names

    # Validate balance input
    try:
        initial_balance = float(initial_balance)
        if initial_balance < 0:
            return None  # Prevent negative balances
    except ValueError:
        return None  # Handle invalid balance input

    new_account = Account(owner_id=owner_id, account_name=account_name, balance=initial_balance)
    
    try:
        db.session.add(new_account)
        db.session.commit()
        return new_account
    except Exception as e:
        db.session.rollback()  # Ensure rollback on failure
        return None

def get_account_by_id(account_id):
    """Retrieve an account by its ID."""
    return Account.query.filter_by(id=account_id).first()

def get_accounts_by_owner(owner_id):
    """Retrieve all accounts belonging to a specific user."""
    return Account.query.filter_by(owner_id=owner_id).all()

def update_account(account_id, account_name=None, balance=None):
    """Update account details such as name or balance."""
    account = Account.query.filter_by(id=account_id).first()
    if not account:
        return None

    if account_name:
        # Ensure account name is unique per owner
        if Account.query.filter_by(owner_id=account.owner_id, account_name=account_name).first():
            return None  # Prevent duplicate account names
        account.account_name = account_name

    if balance is not None:
        try:
            balance = float(balance)
            if balance < 0:
                return None  # Prevent negative balances
            account.balance = balance
        except ValueError:
            return None  # Handle invalid balance input

    try:
        db.session.commit()
        return account
    except Exception:
        db.session.rollback()  # Ensure rollback on failure
        return None

def delete_account(account_id):
    """Delete an account if it exists."""
    account = Account.query.filter_by(id=account_id).first()
    if not account:
        return False

    try:
        db.session.delete(account)
        db.session.commit()
        return True
    except Exception:
        db.session.rollback()  # Ensure rollback on failure
        return False
