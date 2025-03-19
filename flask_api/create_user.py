from app import db, create_app
from models.user_model import User
from models.account_model import Account
from models.transaction_model import Transaction
from models.token_blacklist import TokenBlacklist
from datetime import datetime

# Create and configure the app using your factory
app = create_app()

with app.app_context():
    # Step 1: Create or get mock users
    mock_users = [
        {
            "username": "Badu_warna",
            "email": "badu_warna@gmail.com",
            "password": "password123",
            "address": "123 Ocean View, Jakarta",
            "phone": "081234567890"
        },
        {
            "username": "Lena_Sun",
            "email": "lena_sun@gmail.com",
            "password": "password456",
            "address": "456 Sunrise St, Bali",
            "phone": "082345678901"
        },
        {
            "username": "Jon_Storm",
            "email": "jon_storm@gmail.com",
            "password": "password789",
            "address": "789 Cloudy Rd, Surabaya",
            "phone": "083456789012"
        }
    ]

    created_users = []
    for user_data in mock_users:
        # Check if user already exists to avoid duplicate errors
        user = User.query.filter_by(username=user_data["username"]).first()
        if not user:
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                address=user_data["address"],
                phone=user_data["phone"]
            )
            user.set_password(user_data["password"])
            db.session.add(user)
            db.session.commit()  # Commit immediately to generate the ID
        created_users.append(user)

    # Step 2: Create mock accounts for the users using their actual IDs
    mock_accounts = [
        {
            "owner_id": created_users[0].id,
            "account_name": "Badu Savings Account",
            "balance": 1000.0
        },
        {
            "owner_id": created_users[1].id,
            "account_name": "Lena Checking Account",
            "balance": 500.0
        },
        {
            "owner_id": created_users[2].id,
            "account_name": "Jon Savings Account",
            "balance": 1500.0
        }
    ]

    created_accounts = []
    for account_data in mock_accounts:
        account = Account.query.filter_by(account_name=account_data["account_name"]).first()
        if not account:
            account = Account(
                owner_id=account_data["owner_id"],
                account_name=account_data["account_name"],
                balance=account_data["balance"]
            )
            db.session.add(account)
            db.session.commit()  # Commit to generate account ID
        created_accounts.append(account)

    # Step 3: Create mock transactions for the accounts using their actual IDs
    mock_transactions = [
        {
            "account_id": created_accounts[0].id,
            "amount": 250.0,
            "transaction_type": "deposit",  # Must match the column name in Transaction model
            "timestamp": datetime.now()
        },
        {
            "account_id": created_accounts[1].id,
            "amount": 100.0,
            "transaction_type": "withdrawal",
            "timestamp": datetime.now()
        },
        {
            "account_id": created_accounts[2].id,
            "amount": 500.0,
            "transaction_type": "deposit",
            "timestamp": datetime.now()
        }
    ]

    for tx_data in mock_transactions:
        new_transaction = Transaction(
            account_id=tx_data["account_id"],
            amount=tx_data["amount"],
            transaction_type=tx_data["transaction_type"],
            timestamp=tx_data["timestamp"]
        )
        db.session.add(new_transaction)
    
    db.session.commit()  # Commit transactions

    # Step 4: Create mock blacklisted JWT tokens
    mock_tokens = [
        {"jti": "sample_jti_1", "created_at": datetime.now()},
        {"jti": "sample_jti_2", "created_at": datetime.now()},
        {"jti": "sample_jti_3", "created_at": datetime.now()}
    ]

    for token_data in mock_tokens:
        token = TokenBlacklist.query.filter_by(jti=token_data["jti"]).first()
        if not token:
            token = TokenBlacklist(
                jti=token_data["jti"],
                created_at=token_data["created_at"]
            )
            db.session.add(token)
    
    db.session.commit()  # Final commit for tokens

    print("Mock data has been successfully added to the database!")
