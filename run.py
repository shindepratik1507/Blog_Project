#!/usr/bin/env python3
"""
Blog Writing Platform - Professional Run Script
Complete MCA Mini Project - Error-Free Execution
"""

import os
import sys
import subprocess
from datetime import datetime

def print_header():
    print("="*70)
    print("🚀 BLOG WRITING PLATFORM - MCA MINI PROJECT")
    print("="*70)
    print("📝 Professional Blog Platform with Flask + HTML5 + CSS3 + JavaScript")
    print("🎓 Complete MCA Academic Project - Error-Free Implementation")
    print("⏰ Starting at:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("="*70)

def check_python_version():
    print("\n🔍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible!")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.7+")
        return False

def check_virtual_environment():
    print("\n🔍 Checking virtual environment...")
    if 'VIRTUAL_ENV' in os.environ:
        print(f"✅ Virtual environment active: {os.environ['VIRTUAL_ENV']}")
        return True
    else:
        print("⚠️  No virtual environment detected")
        print("💡 Recommendation: Use a virtual environment")
        print("   python -m venv blog_env")
        print("   source blog_env/bin/activate  # Linux/Mac")
        print("   blog_env\\Scripts\\activate     # Windows")
        return False

def install_dependencies():
    print("\n📦 Installing dependencies...")
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                              capture_output=True, text=True, check=True)
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        print("💡 Try: pip install --upgrade pip")
        return False
    except FileNotFoundError:
        print("❌ requirements.txt not found!")
        return False

def initialize_database():
    print("\n📊 Initializing database...")

    # Check if database already exists
    if os.path.exists('instance/blog_database.db'):
        print("✅ Database already exists!")
        return True

    try:
        result = subprocess.run([sys.executable, 'init_db.py'], 
                              capture_output=True, text=True, check=True)
        print("✅ Database initialized with sample data!")
        print("\n👥 Sample Login Credentials:")
        print("   📧 rajesh@example.com | 🔑 password123")
        print("   📧 priya@example.com  | 🔑 password123")
        print("   📧 amit@example.com   | 🔑 password123")
        print("   📧 sneha@example.com  | 🔑 password123")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error initializing database: {e}")
        return False
    except FileNotFoundError:
        print("❌ init_db.py not found!")
        return False

def check_files():
    print("\n📁 Checking project files...")
    required_files = [
        'app.py',
        'requirements.txt',
        'init_db.py',
        'static/css/style.css',
        'static/js/script.js',
        'templates/base.html',
        'templates/index.html'
    ]

    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MISSING!")
            missing_files.append(file)

    if missing_files:
        print(f"\n❌ Missing {len(missing_files)} required files!")
        return False
    else:
        print("✅ All required files present!")
        return True

def start_application():
    print("\n🌐 Starting Flask application...")
    print("="*50)
    print("🎯 Application will be available at:")
    print("   🔗 http://localhost:5000")
    print("   🔗 http://127.0.0.1:5000")
    print("="*50)
    print("📝 Features available:")
    print("   ✅ User Registration & Login")
    print("   ✅ Blog Writing & Publishing")
    print("   ✅ Image Upload Support")
    print("   ✅ Search & Like Functionality")
    print("   ✅ Responsive Design")
    print("   ✅ Professional UI/UX")
    print("="*50)
    print("🎓 MCA Mini Project - Ready for Demonstration!")
    print("⏹️  Press Ctrl+C to stop the server")
    print("="*50)

    try:
        # Import and run the Flask app
        from app import app
        app.run(debug=True, port=5000, host='127.0.0.1')
    except ImportError as e:
        print(f"❌ Error importing Flask app: {e}")
        print("💡 Make sure you've installed the requirements:")
        print("   pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False

    return True

def main():
    print_header()

    # Check system requirements
    if not check_python_version():
        sys.exit(1)

    # Check virtual environment (optional)
    check_virtual_environment()

    # Check required files
    if not check_files():
        print("\n❌ Project setup incomplete!")
        sys.exit(1)

    # Install dependencies
    if not install_dependencies():
        print("\n❌ Failed to install dependencies!")
        sys.exit(1)

    # Initialize database
    if not initialize_database():
        print("\n❌ Failed to initialize database!")
        sys.exit(1)

    print("\n🎉 Setup completed successfully!")
    print("\n" + "="*50)

    # Start the application
    if not start_application():
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped by user")
        print("🎓 Thank you for using Blog Writing Platform!")
        print("💯 Perfect for MCA Mini Project Submission!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
