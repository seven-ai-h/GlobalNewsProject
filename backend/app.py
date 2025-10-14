from flask import Flask, render_template, jsonify, request
from googletrans import Translator
from textblob import TextBlob
from langdetect import detect, detect_langs
import re

app = Flask(__name__)
translator = Translator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    try:
        data = request.json
        text = data.get('text', '')
        src_lang = data.get('from', 'auto')
        trg_lang = data.get('to', 'en')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Perform translation
        result = translator.translate(text, src=src_lang, dest=trg_lang)
        
        return jsonify({
            'translation': result.text,
            'src_lang': result.src,
            'dest_lang': result.dest
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/detect', methods=['POST'])
def detect_language():
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Use langdetect for better confidence scores
        detected_langs = detect_langs(text)
        primary_lang = detected_langs[0]
        
        # Language name mapping
        lang_names = {
            'en': 'English',
            'zh-cn': 'Chinese (Simplified)',
            'zh-tw': 'Chinese (Traditional)',
            'ja': 'Japanese',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'ko': 'Korean',
            'ar': 'Arabic',
            'hi': 'Hindi',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'it': 'Italian'
        }
        
        lang_code = primary_lang.lang
        lang_name = lang_names.get(lang_code, lang_code.upper())
        
        return jsonify({
            'language': lang_code,
            'language_name': lang_name,
            'confidence': round(primary_lang.prob, 4),
            'all_detected': [{'lang': l.lang, 'confidence': round(l.prob, 4)} for l in detected_langs[:3]]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/sentiment', methods=['POST'])
def analyze_sentiment():
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Detect language first
        try:
            lang = detect(text)
        except:
            lang = 'en'
        
        # For non-English text, translate to English for sentiment analysis
        analysis_text = text
        if lang not in ['en']:
            try:
                translated = translator.translate(text, dest='en')
                analysis_text = translated.text
            except:
                pass  # If translation fails, try analyzing original text
        
        # Perform sentiment analysis
        blob = TextBlob(analysis_text)
        polarity = blob.sentiment.polarity  # -1 to 1
        subjectivity = blob.sentiment.subjectivity  # 0 to 1
        
        # Determine sentiment label
        if polarity > 0.1:
            sentiment = 'Positive'
            emoji = '😊'
        elif polarity < -0.1:
            sentiment = 'Negative'
            emoji = '😔'
        else:
            sentiment = 'Neutral'
            emoji = '😐'
        
        # Calculate confidence (higher subjectivity or stronger polarity = higher confidence)
        confidence = min(abs(polarity) + (subjectivity * 0.5), 1.0)
        
        return jsonify({
            'sentiment': sentiment,
            'emoji': emoji,
            'polarity': round(polarity, 3),
            'subjectivity': round(subjectivity, 3),
            'confidence': round(confidence, 3),
            'language': lang,
            'analysis_text': analysis_text if lang != 'en' else None
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)