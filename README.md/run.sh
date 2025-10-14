#!/bin/bash

echo "🌍 GlobalNews Translation App - Starting..."
echo ""

# Navigate to backend directory
cd "$(dirname "$0")/../backend"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Run the application
echo ""
echo "✨ Starting Flask application..."
echo "🌐 Open your browser and go to: http://localhost:5000"
echo ""
python app.py

