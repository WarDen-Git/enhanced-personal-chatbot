#!/usr/bin/env python3
"""
Enhanced Chatbot - Deployment Helper Script
Helps set up the application for various deployment platforms.
"""
import os
import shutil
from pathlib import Path

def create_gitignore():
    """Create .gitignore file for safe repository management."""
    gitignore_content = """
# Environment variables
.env
.streamlit/secrets.toml

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg

# Database files (optional - remove if you want to keep data)
*.db
*.sqlite
*.sqlite3

# Logs
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Temporary files
tmp/
temp/
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content.strip())
    
    print("✅ Created .gitignore file")

def setup_streamlit_cloud():
    """Set up files for Streamlit Cloud deployment."""
    print("🚀 Setting up for Streamlit Cloud deployment...")
    
    # Check if secrets template exists
    secrets_file = Path('.streamlit/secrets.toml')
    if secrets_file.exists():
        print(f"✅ Streamlit secrets template ready at {secrets_file}")
        print("📝 Remember to:")
        print("   1. Push code to GitHub")
        print("   2. Go to share.streamlit.io") 
        print("   3. Connect your repository")
        print("   4. Add your API keys in the Streamlit Cloud dashboard")
        print("   5. Deploy!")
    else:
        print("❌ Streamlit configuration not found")

def setup_docker():
    """Set up files for Docker deployment."""
    print("🐳 Setting up for Docker deployment...")
    
    dockerfile = Path('Dockerfile')
    if dockerfile.exists():
        print("✅ Dockerfile ready")
        print("🔧 To build and run locally:")
        print("   docker build -t enhanced-chatbot .")
        print("   docker run -p 8501:8501 --env-file .env enhanced-chatbot")
    else:
        print("❌ Dockerfile not found")

def setup_railway():
    """Set up files for Railway deployment."""  
    print("🚂 Setting up for Railway deployment...")
    
    railway_config = Path('railway.json')
    if railway_config.exists():
        print("✅ Railway configuration ready")
        print("🔧 To deploy:")
        print("   1. Install Railway CLI: npm install -g @railway/cli")
        print("   2. Login: railway login")
        print("   3. Deploy: railway up")
    else:
        print("❌ Railway configuration not found")

def check_environment():
    """Check if environment is properly configured."""
    print("🔍 Checking environment configuration...")
    
    env_file = Path('.env')
    if not env_file.exists():
        print("⚠️  .env file not found - copy from .env.example")
        return False
    
    # Check for required environment variables
    with open(env_file, 'r') as f:
        content = f.read()
    
    if 'your_openai_api_key_here' in content:
        print("⚠️  Please update your OpenAI API key in .env file")
        return False
    
    print("✅ Environment configuration looks good")
    return True

def prepare_for_deployment():
    """Prepare the application for deployment."""
    print("🎯 Preparing Enhanced Chatbot for deployment...")
    print("=" * 60)
    
    # Create .gitignore
    create_gitignore()
    
    # Check environment
    env_ready = check_environment()
    
    print("\\n📋 Deployment options available:")
    print("1. Streamlit Cloud (Free & Recommended)")
    print("2. Docker (Any cloud provider)")
    print("3. Railway (Professional)")
    print("4. Local network sharing")
    
    choice = input("\\nWhich deployment option? (1-4): ").strip()
    
    if choice == '1':
        setup_streamlit_cloud()
    elif choice == '2':
        setup_docker()
    elif choice == '3':
        setup_railway()
    elif choice == '4':
        print("🏠 Local network sharing:")
        print("   streamlit run app.py --server.address 0.0.0.0")
        print("   Others can access via: http://YOUR_LOCAL_IP:8501")
    else:
        print("ℹ️  See DEPLOYMENT.md for detailed instructions")
    
    print("\\n📚 For detailed guides, check DEPLOYMENT.md")
    
    if not env_ready:
        print("\\n⚠️  Please configure your .env file before deploying!")

def main():
    """Main function."""
    prepare_for_deployment()

if __name__ == "__main__":
    main()