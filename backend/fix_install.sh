#!/bin/bash

echo "🔧 GlobalNews Translation App - Installation Fix"
echo "=================================================="
echo ""

# Navigate to backend directory
cd "$(dirname "$0")"

echo "📍 Current directory: $(pwd)"
echo ""

# Check Python version
echo "🐍 Checking Python..."
python3 --version
echo ""

# Install packages with --user flag (avoids permission issues)
echo "📦 Installing Python packages (with --user flag)..."
pip3 install --user Flask==2.3.0
pip3 install --user googletrans==4.0.0rc1
pip3 install --user Werkzeug==2.3.0
pip3 install --user textblob==0.17.1
pip3 install --user langdetect==1.0.9

echo ""
echo "✅ Packages installed!"
echo ""

# Download NLTK data to user directory
echo "📥 Downloading NLP data..."
python3 << 'EOF'
import nltk
import os

download_dir = os.path.expanduser('~/nltk_data')
print(f"Downloading to: {download_dir}")

try:
    nltk.download('punkt', download_dir=download_dir, quiet=True)
    nltk.download('brown', download_dir=download_dir, quiet=True)
    print("✅ NLP data downloaded successfully!")
except Exception as e:
    print(f"⚠️  Warning: {e}")
    print("You may need to download manually later.")
EOF

echo ""
echo "🧪 Testing installation..."
python3 << 'EOF'
try:
    import flask
    from googletrans import Translator
    from textblob import TextBlob
    from langdetect import detect
    
    print("✅ Flask:", flask.__version__)
    print("✅ googletrans: OK")
    print("✅ textblob: OK")
    print("✅ langdetect: OK")
    print("")
    print("🎉 All packages installed successfully!")
except ImportError as e:
    print("❌ Error:", e)
    exit(1)
EOF

echo ""
echo "=================================================="
echo "✅ Installation complete!"
echo ""
echo "To run the app:"
echo "  python3 app.py"
echo ""
echo "Then open: http://localhost:5000"
echo "=================================================="

