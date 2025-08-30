#!/usr/bin/env python3
"""
Enhanced Personal Chatbot - Startup Script
"""
import sys
import os
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if all required dependencies are installed."""
    required_packages = [
        'streamlit', 'openai', 'python-dotenv', 'pypdf', 
        'plotly', 'pandas', 'requests', 'pydantic'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Please install them using: pip install -r requirements.txt")
        return False
    
    print("✅ All required packages are installed")
    return True

def check_environment():
    """Check if environment variables are set."""
    required_vars = ['OPENAI_API_KEY']
    optional_vars = ['PUSHOVER_TOKEN', 'PUSHOVER_USER']
    
    missing_required = []
    missing_optional = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_required.append(var)
    
    for var in optional_vars:
        if not os.getenv(var):
            missing_optional.append(var)
    
    if missing_required:
        print(f"❌ Missing required environment variables: {', '.join(missing_required)}")
        print("Please create a .env file based on .env.example")
        return False
    
    print("✅ Required environment variables are set")
    
    if missing_optional:
        print(f"⚠️  Optional environment variables not set: {', '.join(missing_optional)}")
        print("Some features may be limited without these")
    
    return True

def setup_directories():
    """Create necessary directories."""
    directories = [
        'data/documents',
        'data/analytics', 
        'static/css',
        'static/js'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Directories created successfully")

def main():
    """Main startup function."""
    print("🤖 Enhanced Personal Chatbot - Starting up...")
    print("=" * 50)
    
    # Change to script directory
    os.chdir(Path(__file__).parent)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Setup directories
    setup_directories()
    
    print("=" * 50)
    print("🚀 Starting the application...")
    print("📊 Access the chatbot at: http://localhost:8501")
    print("💡 Use Ctrl+C to stop the application")
    print("=" * 50)
    
    try:
        # Start Streamlit application
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.address", "localhost",
            "--server.port", "8501",
            "--server.headless", "false"
        ])
    except KeyboardInterrupt:
        print("\\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()