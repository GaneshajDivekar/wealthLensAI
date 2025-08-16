#!/usr/bin/env python3
"""
Setup script for Financial Portfolio Analysis System
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def create_virtual_environment():
    """Create virtual environment"""
    if os.path.exists(".venv"):
        print("✅ Virtual environment already exists")
        return True
    
    return run_command("python -m venv .venv", "Creating virtual environment")

def activate_virtual_environment():
    """Activate virtual environment"""
    if os.name == 'nt':  # Windows
        activate_script = ".venv\\Scripts\\activate"
    else:  # Unix/Linux/macOS
        activate_script = ".venv/bin/activate"
    
    if os.path.exists(activate_script):
        print("✅ Virtual environment ready")
        return True
    else:
        print("❌ Virtual environment not found")
        return False

def install_dependencies():
    """Install required dependencies"""
    if os.name == 'nt':  # Windows
        pip_cmd = ".venv\\Scripts\\pip"
    else:  # Unix/Linux/macOS
        pip_cmd = ".venv/bin/pip"
    
    return run_command(f"{pip_cmd} install -r requirements.txt", "Installing dependencies")

def create_env_file():
    """Create .env file with template"""
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    env_content = """# API Keys (Get free keys from respective services)
MISTRAL_API_KEY=your_mistral_api_key_here
NEWS_API_KEY=your_news_api_key_here
GOOGLE_API_KEY=your_google_api_key_here

# Database Configuration
CHROMA_DB_PATH=./chroma_db

# Optional: Override default settings
# PORTFOLIO_VALUE=8000000
# CURRENCY=INR
"""
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ Created .env file with template")
        print("⚠️  Please update the API keys in .env file")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ["chroma_db", "logs"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    print("✅ Created necessary directories")
    return True

def check_api_keys():
    """Check if API keys are configured"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        mistral_key = os.getenv("MISTRAL_API_KEY")
        if mistral_key and mistral_key != "your_mistral_api_key_here":
            print("✅ Mistral API key is configured")
            return True
        else:
            print("⚠️  Mistral API key not configured")
            print("   Get a free key from: https://console.mistral.ai/")
            return False
    except ImportError:
        print("⚠️  python-dotenv not installed")
        return False

def run_quick_test():
    """Run a quick test to verify installation"""
    print("\n🧪 Running quick test...")
    
    try:
        # Test imports
        import fastapi
        import langgraph
        import chromadb
        print("✅ All core dependencies imported successfully")
        
        # Test configuration
        from config import Config
        print("✅ Configuration loaded successfully")
        
        # Test data
        from data import get_portfolio_summary
        summary = get_portfolio_summary()
        print(f"✅ Portfolio data loaded: ₹{summary['total_value']:,.0f}")
        
        return True
    except Exception as e:
        print(f"❌ Quick test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Financial Portfolio Analysis System - Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Create virtual environment
    if not create_virtual_environment():
        return False
    
    # Activate virtual environment
    if not activate_virtual_environment():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Create directories
    if not create_directories():
        return False
    
    # Create .env file
    if not create_env_file():
        return False
    
    # Check API keys
    check_api_keys()
    
    # Run quick test
    if not run_quick_test():
        print("⚠️  Setup completed with warnings")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Update API keys in .env file")
    print("2. Start the server: python main.py")
    print("3. Run tests: python test_system.py")
    print("4. Open API docs: http://localhost:8000/docs")
    print("\n📚 Documentation:")
    print("- README.md: Complete setup and usage guide")
    print("- demo_script.md: Tech conference demo script")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
