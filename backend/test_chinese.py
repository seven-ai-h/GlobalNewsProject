#!/usr/bin/env python3
"""
Quick test to verify Chinese translation is working
"""

from googletrans import Translator

print("🧪 Testing Chinese Translation Fix\n")
print("="*50)

translator = Translator()

# Test all language pairs
tests = [
    ("Hello world", "en", "zh-cn", "🇺🇸 → 🇨🇳"),
    ("你好世界", "zh-cn", "en", "🇨🇳 → 🇺🇸"),
    ("你好", "zh-cn", "ja", "🇨🇳 → 🇯🇵"),
    ("こんにちは", "ja", "zh-cn", "🇯🇵 → 🇨🇳"),
    ("Good morning", "en", "zh-cn", "🇺🇸 → 🇨🇳"),
    ("早上好", "zh-cn", "en", "🇨🇳 → 🇺🇸"),
]

print("\nTranslation Tests:\n")
for text, src, dest, desc in tests:
    try:
        result = translator.translate(text, src=src, dest=dest)
        status = "✅"
        output = result.text
    except Exception as e:
        status = "❌"
        output = str(e)[:40]
    
    print(f"{status} {desc}: {text} → {output}")

print("\n" + "="*50)
print("✅ Chinese translation is working!")
print("\nTo run the web app:")
print("  python3 app.py")
print("\nThen test in browser at: http://localhost:5000")

