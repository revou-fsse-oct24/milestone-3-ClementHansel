from models import db
from models.account_model import Account


def validate_balance(balance):
    """Helper function to validate if the balance is valid (non-negative and numeric)."""
    try:
        balance = float(balance)
        if balance < 0:
            return False, "Balance cannot be negative."
        return True, balance
    except ValueError:
        return False, "Invalid balance format."


def create_account(owner_id, account_name=None, initial_balance=0.0):
    """Create a new account for a user, ensuring account name uniqueness."""
    if Account.query.filter_by(owner_id=owner_id, account_name=account_name).first():
        return None, "Account name already exists for this user."

    is_valid, message = validate_balance(initial_balance)
    if not is_valid:
        return None, message  # Return error message if balance is invalid

    new_account = Account(owner_id=owner_id, account_name=account_name, balance=message)
    
    try:
        db.session.add(new_account)
        db.session.commit()
        return new_account, None
    except Exception as e:
        db.session.rollback()  # Ensure rollback on failure
        return None, f"Error creating account: {str(e)}"  # Return the error message


def get_account_by_id(account_id):
    """Retrieve an account by its ID."""
    account = Account.query.filter_by(id=account_id).first()
    if account:
        return account, None
    return None, "Account not found."


def get_accounts_by_owner(owner_id):
    """Retrieve all accounts belonging to a specific user."""
    accounts = Account.query.filter_by(owner_id=owner_id).all()
    if accounts:
        return accounts, None
    return [], "No accounts found for this user."


def update_account(account_id, account_name=None, balance=None):
    """Update account details such as name or balance."""
    account = Account.query.filter_by(id=account_id).first()
    if not account:
        return None, "Account not found."

    if account_name:
        # Ensure account name is unique per owner
        if Account.query.filter_by(owner_id=account.owner_id, account_name=account_name).first():
            return None, "Account name already exists for this user."
        account.account_name = account_name

    if balance is not None:
        is_valid, validated_balance = validate_balance(balance)
        if not is_valid:
            return None, validated_balance  # Return error message if balance is invalid
        account.balance = validated_balance

    try:
        db.session.commit()
        return account, None
    except Exception as e:
        db.session.rollback()  # Ensure rollback on failure
        return None, f"Error updating account: {str(e)}"


def delete_account(account_id):
    """Delete an account if it exists."""
    account = Account.query.filter_by(id=account_id).first()
    if not account:
        return False, "Account not found."

    try:
        db.session.delete(account)
        db.session.commit()
        return True, None
    except Exception as e:
        db.session.rollback()  # Ensure rollback on failure
        return False, f"Error deleting account: {str(e)}"
