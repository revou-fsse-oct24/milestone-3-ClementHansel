from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db
from models.account_model import Account
from models.transaction_model import Transaction
from datetime import datetime

transaction_bp = Blueprint('transaction_bp', __name__, url_prefix='/transactions')

@transaction_bp.route('', methods=['POST'])
@jwt_required()
def create_transaction():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    # Validate transaction type
    if data["type"] not in ["withdrawal", "deposit", "transfer"]:
        return jsonify({"error": "Invalid transaction type"}), 400

    account = Account.query.get(data["account_id"])
    if not account or account.owner_id != user_id:
        return jsonify({"error": "Unauthorized: You do not own this account"}), 403

    if data["type"] == "withdrawal":
        if account.balance < data["amount"]:
            return jsonify({"error": "Insufficient funds"}), 400
        account.balance -= data["amount"]

    elif data["type"] == "deposit":
        account.balance += data["amount"]

    elif data["type"] == "transfer":
        if "receiver_account_id" not in data:
            return jsonify({"error": "Receiver account ID required for transfers"}), 400
        
        receiver_account = Account.query.get(data["receiver_account_id"])
        if not receiver_account:
            return jsonify({"error": "Receiver account not found"}), 404
        if account.id == receiver_account.id:
            return jsonify({"error": "Cannot transfer to the same account"}), 400
        if account.balance < data["amount"]:
            return jsonify({"error": "Insufficient funds"}), 400
        
        # Perform transfer
        account.balance -= data["amount"]
        receiver_account.balance += data["amount"]
        db.session.add(receiver_account)

    transaction = Transaction(
        account_id=account.id,
        amount=data["amount"],
        type=data["type"]
    )

    db.session.add(account)
    db.session.add(transaction)
    db.session.commit()
    
    return jsonify({"transaction_id": transaction.id}), 201

@transaction_bp.route('', methods=['GET'])
@jwt_required()
def get_transactions():
    """Retrieve transactions with optional filters: account_id, start_date, end_date."""
    user_id = int(get_jwt_identity())
    user_accounts = Account.query.filter_by(owner_id=user_id).all()
    account_ids = [acc.id for acc in user_accounts]

    # Get query parameters
    account_id = request.args.get("account_id", type=int)
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    # Start the base query
    query = Transaction.query.filter(Transaction.account_id.in_(account_ids))

    # Apply filters
    if account_id:
        if account_id not in account_ids:
            return jsonify({"error": "Unauthorized: You do not own this account"}), 403
        query = query.filter(Transaction.account_id == account_id)

    if start_date:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            query = query.filter(Transaction.timestamp >= start_date)
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    if end_date:
        try:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            query = query.filter(Transaction.timestamp <= end_date)
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    # Execute query
    transactions = query.all()

    return jsonify([{
        "id": t.id,
        "account_id": t.account_id,
        "amount": t.amount,
        "type": t.type,
        "timestamp": t.timestamp.isoformat()
    } for t in transactions]), 200

@transaction_bp.route('/<int:transaction_id>', methods=['GET'])
@jwt_required()
def get_transaction(transaction_id):
    user_id = int(get_jwt_identity())
    transaction = Transaction.query.get(transaction_id)

    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404
  
    account = Account.query.get(transaction.account_id)
    if not account or account.owner_id != user_id:
        return jsonify({"error": "Unauthorized: You do not own this account"}), 403

    return jsonify({
        "id": transaction.id,
        "account_id": transaction.account_id,
        "amount": transaction.amount,
        "type": transaction.type,
        "timestamp": transaction.timestamp.isoformat()
    }), 200
