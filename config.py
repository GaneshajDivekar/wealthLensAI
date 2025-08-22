import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "your_mistral_api_key_here")
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "your_news_api_key_here")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "your_google_api_key_here")

# Database Configuration
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")

# WealthLens Configuration
PORTFOLIO_VALUE = 8000000  # 80 lacs INR
CURRENCY = "INR"

# User Information
USER_NAME = "Ganesh Divekar"
USER_COMPANY = "Bajaj Technology"
USER_ROLE = "Leading India USA Mideast AI Team"
USER_CONTACT = "8459684546"

# Authentication Credentials (Disabled for demo)
AUTHENTICATION_ENABLED = False
DEFAULT_USERNAME = "demo"
DEFAULT_PASSWORD = "demo123"
DEMO_USERNAME = "demo"
DEMO_PASSWORD = "demo123"

# Users Database (in production, use proper database)
USERS = {
    "admin": {
        "password": "wealthlens2024",
        "role": "admin",
        "name": "System Administrator",
        "email": "admin@wealthlens.com"
    },
    "demo": {
        "password": "demo123",
        "role": "user",
        "name": "Demo User",
        "email": "demo@wealthlens.com"
    },
    "ganesh": {
        "password": "ganesh123",
        "role": "user",
        "name": "Ganesh Divekar",
        "email": "ganesh@bajajtechnology.com"
    }
}
