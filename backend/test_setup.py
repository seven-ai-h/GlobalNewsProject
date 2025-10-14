#!/usr/bin/env python3
"""
Quick test script to verify all dependencies are installed correctly
"""

print("🧪 Testing GlobalNews Translation App Setup...\n")

# Test 1: Flask
try:
    import flask
    print("✅ Flask installed:", flask.__version__)
except ImportError as e:
    print("❌ Flask not installed:", str(e))

# Test 2: googletrans
try:
    from googletrans import Translator
    print("✅ googletrans installed")
except ImportError as e:
    print("❌ googletrans not installed:", str(e))

# Test 3: TextBlob
try:
    from textblob import TextBlob
    print("✅ TextBlob installed")
    
    # Test sentiment analysis
    test_text = TextBlob("I love this!")
    sentiment = test_text.sentiment
    print(f"   └─ Sentiment test: polarity={sentiment.polarity}, subjectivity={sentiment.subjectivity}")
except ImportError as e:
    print("❌ TextBlob not installed:", str(e))
except Exception as e:
    print(f"⚠️  TextBlob installed but needs data. Run: python -m textblob.download_corpora")

# Test 4: langdetect
try:
    from langdetect import detect, detect_langs
    print("✅ langdetect installed")
    
    # Test detection
    test_lang = detect("Hello world")
    print(f"   └─ Detection test: 'Hello world' → {test_lang}")
except ImportError as e:
    print("❌ langdetect not installed:", str(e))

# Test 5: Werkzeug
try:
    import werkzeug
    print("✅ Werkzeug installed:", werkzeug.__version__)
except ImportError as e:
    print("❌ Werkzeug not installed:", str(e))

print("\n" + "="*50)

# Final check
try:
    from flask import Flask
    from googletrans import Translator
    from textblob import TextBlob
    from langdetect import detect
    
    print("✅ All required packages installed!")
    print("\n📝 Next steps:")
    print("   1. Download TextBlob data:")
    print("      python -c \"import nltk; nltk.download('punkt'); nltk.download('brown')\"")
    print("   2. Run the app:")
    print("      python app.py")
    print("   3. Open browser:")
    print("      http://localhost:5000")
except ImportError:
    print("❌ Some packages are missing. Install them with:")
    print("   pip install -r requirements.txt")

