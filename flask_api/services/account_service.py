from models import db
from models.account_model import Account


def create_account(owner_id, account_name=None, initial_balance=0.0):
    new_account = Account(owner_id=owner_id, account_name=account_name, balance=initial_balance)
    db.session.add(new_account)
    db.session.commit()
    return new_account

def get_account_by_id(account_id):
    return Account.query.get(account_id)

def get_accounts_by_owner(owner_id):
    return Account.query.filter_by(owner_id=owner_id).all()

def update_account(account_id, account_name=None, balance=None):
    account = Account.query.get(account_id)
    if not account:
        return None
    if account_name is not None:
        account.account_name = account_name
    if balance is not None:
        account.balance = balance
    db.session.commit()
    return account

def delete_account(account_id):
    account = Account.query.get(account_id)
    if not account:
        return False
    db.session.delete(account)
    db.session.commit()
    return True
