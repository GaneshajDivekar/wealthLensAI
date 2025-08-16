import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "6Mb8kTLH8GbFWbXYnvup8m1MmKkGKvY4")
    NEWS_API_KEY = os.getenv("NEWS_API_KEY", "102a73f9d30b4a2a918b56efe368bd20")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyDWRyP01tuMYeRBtVOB87FV-DfHqWTqN8o")
    CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")
    
        # WealthLens Configuration
    PORTFOLIO_VALUE = 8000000  # 80 lacs in INR
    CURRENCY = "INR"
    
    # User Information
    USER_NAME = "Ganesh Divekar"
    USER_COMPANY = "Bajaj Technology"
    USER_ROLE = "Leading India USA Mideast AI Team"
    USER_CONTACT = "8459684546"
