from models import db

class TokenBlacklist(db.Model):
    """Stores blacklisted JWT tokens."""
    __tablename__ = "token_blacklist"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(255), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
