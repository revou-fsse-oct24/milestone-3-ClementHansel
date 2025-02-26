import os
from dotenv import load_dotenv
from datetime import timedelta

# Load environment variables from .env
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Flask application configuration."""
    
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_fallback_secret_key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_fallback_jwt_key')
   
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "data", "db.sqlite3").replace("\\", "/")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", "3600").strip()))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", "86400").strip()))

    CORS_HEADERS = "Content-Type"
    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() in ["true", "1"]

print(f"DATABASE_URL (Final): {Config.SQLALCHEMY_DATABASE_URI}")
