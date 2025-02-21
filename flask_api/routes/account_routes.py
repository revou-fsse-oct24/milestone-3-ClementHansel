from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db
from models.account_model import Account

account_bp = Blueprint('account_bp', __name__, url_prefix='/accounts')

@account_bp.route('', methods=['POST'])
@jwt_required()
def create_account():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    balance = data.get("initial_balance", 0.0)
    account_name = data.get("account_name")
    account = Account(owner_id=user_id, balance=balance, account_name=account_name)
    db.session.add(account)
    db.session.commit()
    return jsonify({"account_id": account.id}), 201

@account_bp.route('', methods=['GET'])
@jwt_required()
def get_accounts():
    user_id = int(get_jwt_identity())
    accounts = Account.query.filter_by(owner_id=user_id).all()
    return jsonify([{"id": acc.id, "account_name": acc.account_name, "balance": acc.balance} for acc in accounts]), 200

@account_bp.route('/<int:account_id>', methods=['GET'])
@jwt_required()
def get_account(account_id):
    """Retrieve details of a specific account by its ID."""
    user_id = int(get_jwt_identity())
    account = Account.query.get(account_id)
    if not account:
        return jsonify({"error": "Account not found"}), 404
    if account.owner_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403
    return jsonify({"id": account.id, "account_name": account.account_name, "balance": account.balance}), 200

@account_bp.route('/<int:account_id>', methods=['PUT'])
@jwt_required()
def update_account(account_id):
    """Update details of an existing account (only if owned by the authenticated user)."""
    user_id = int(get_jwt_identity())
    account = Account.query.get(account_id)
    if not account:
        return jsonify({"error": "Account not found"}), 404
    if account.owner_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    if "account_name" in data:
        account.account_name = data["account_name"]
    if "initial_balance" in data:
        account.balance = data["initial_balance"]

    db.session.commit()
    return jsonify({
        "message": "Account updated", 
        "id": account.id, 
        "account_name": account.account_name, 
        "balance": account.balance
    }), 200

@account_bp.route('/<int:account_id>', methods=['DELETE'])
@jwt_required()
def delete_account(account_id):
    """Delete an account if the authenticated user is the owner."""
    user_id = int(get_jwt_identity())
    account = Account.query.get(account_id)
    if not account:
        return jsonify({"error": "Account not found"}), 404
    if account.owner_id != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    db.session.delete(account)
    db.session.commit()
    return jsonify({"message": "Account deleted", "id": account_id}), 200
