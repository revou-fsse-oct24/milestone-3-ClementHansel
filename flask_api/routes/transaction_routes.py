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
    """Create a new transaction (deposit, withdrawal, or transfer)."""
    user_id = int(get_jwt_identity())
    data = request.get_json()

    transaction_type = data.get("transaction_type")  # Renamed from "type"
    amount = data.get("amount")
    account_id = data.get("account_id")

    # Validate transaction type
    if transaction_type not in ["withdrawal", "deposit", "transfer"]:
        return jsonify({"error": "Invalid transaction type"}), 400

    # Validate amount
    if not isinstance(amount, (int, float)) or amount <= 0:
        return jsonify({"error": "Amount must be a positive number"}), 400

    account = Account.query.filter_by(id=account_id, owner_id=user_id).first()
    if not account:
        return jsonify({"error": "Unauthorized: You do not own this account"}), 403

    if transaction_type == "withdrawal":
        if account.balance < amount:
            return jsonify({"error": "Insufficient funds"}), 400
        account.balance -= amount

    elif transaction_type == "deposit":
        account.balance += amount

    elif transaction_type == "transfer":
        receiver_account_id = data.get("receiver_account_id")

        if not receiver_account_id:
            return jsonify({"error": "Receiver account ID required for transfers"}), 400
        
        receiver_account = Account.query.filter_by(id=receiver_account_id).first()
        if not receiver_account:
            return jsonify({"error": "Receiver account not found"}), 404
        if account.id == receiver_account.id:
            return jsonify({"error": "Cannot transfer to the same account"}), 400
        if account.balance < amount:
            return jsonify({"error": "Insufficient funds"}), 400

        # Perform transfer
        account.balance -= amount
        receiver_account.balance += amount

        # Create transaction records for both sender and receiver
        sender_transaction = Transaction(
            account_id=account.id,
            amount=amount,
            transaction_type="transfer_out"
        )
        receiver_transaction = Transaction(
            account_id=receiver_account.id,
            amount=amount,
            transaction_type="transfer_in"
        )

        db.session.add(receiver_account)
        db.session.add(receiver_transaction)

    # Store transaction record
    transaction = Transaction(
        account_id=account.id,
        amount=amount,
        transaction_type=transaction_type
    )

    try:
        db.session.add(account)
        db.session.add(transaction)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500

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
        "amount": str(t.amount),  # Convert Numeric to string for JSON response
        "transaction_type": t.transaction_type,
        "timestamp": t.timestamp.isoformat()
    } for t in transactions]), 200

@transaction_bp.route('/<int:transaction_id>', methods=['GET'])
@jwt_required()
def get_transaction(transaction_id):
    """Retrieve details of a specific transaction."""
    user_id = int(get_jwt_identity())
    transaction = Transaction.query.filter_by(id=transaction_id).first()

    if not transaction:
        return jsonify({"error": "Transaction not found"}), 404
  
    account = Account.query.filter_by(id=transaction.account_id, owner_id=user_id).first()
    if not account:
        return jsonify({"error": "Unauthorized: You do not own this account"}), 403

    return jsonify({
        "id": transaction.id,
        "account_id": transaction.account_id,
        "amount": str(transaction.amount),
        "transaction_type": transaction.transaction_type,
        "timestamp": transaction.timestamp.isoformat()
    }), 200
