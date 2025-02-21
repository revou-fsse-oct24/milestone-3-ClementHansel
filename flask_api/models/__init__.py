from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models after db is created
from .user_model import User
from .account_model import Account
from .transaction_model import Transaction
