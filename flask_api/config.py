import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Flask application configuration."""
 
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_fallback_secret_key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_fallback_jwt_key')
  
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_HEADER_NAME = "Authorization"
    JWT_HEADER_TYPE = "Bearer"
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 3600))
    JWT_REFRESH_TOKEN_EXPIRES = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", 86400))
 
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("DATABASE_URL is not set in the environment variables")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    CORS_HEADERS = "Content-Type"
 
    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() in ["true", "1"]

