from models import db

class TokenBlacklist(db.Model):
    """Stores blacklisted JWT tokens."""
    __tablename__ = "token_blacklist"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(255), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

    # Adding index to created_at for faster queries
    __table_args__ = (
        db.Index('ix_token_blacklist_created_at', 'created_at'),  # Index for faster queries based on creation time
    )

    def __repr__(self):
        return f"<TokenBlacklist(id={self.id}, jti={self.jti}, created_at={self.created_at})>"
