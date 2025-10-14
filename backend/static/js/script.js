function showTab(event, tabName) {
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
}

const languageNames = {
    en: 'English', 
    'zh-cn': 'Chinese (Simplified)',
    'zh-tw': 'Chinese (Traditional)', 
    zh: 'Chinese',
    ja: 'Japanese'
};

async function detectLanguage() {
    const text = document.getElementById('languageText').value.trim();
    if (!text) return alert('Please enter text to analyze');

    try {
        const response = await fetch('/detect', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });

        const data = await response.json();
        
        if (data.error) {
            alert(`Error: ${data.error}`);
            return;
        }
        
        const langName = data.language_name || data.language.toUpperCase();
        const confidence = (data.confidence * 100).toFixed(1);
        
        let html = `
            <h3>🌍 Detected Language: ${langName}</h3>
            <p><strong>Confidence:</strong> ${confidence}%</p>
            <div class="confidence-bar">
                <div class="confidence-fill" style="width: ${confidence}%"></div>
            </div>
        `;
        
        // Show alternative detections if available
        if (data.all_detected && data.all_detected.length > 1) {
            html += '<p style="margin-top: 1rem;"><strong>Other possible languages:</strong></p><ul>';
            data.all_detected.slice(1).forEach(lang => {
                html += `<li>${lang.lang}: ${(lang.confidence * 100).toFixed(1)}%</li>`;
            });
            html += '</ul>';
        }
        
        document.getElementById('languageResult').innerHTML = html;
        document.getElementById('languageResult').classList.remove('hidden');
    } catch (error) {
        console.error('Error:', error);
        alert('Language detection failed. Please try again.');
    }
}

async function analyzeSentiment() {
    const text = document.getElementById('sentimentText').value.trim();
    if (!text) return alert('Please enter text to analyze');

    try {
        const response = await fetch('/sentiment', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });

        const data = await response.json();
        
        if (data.error) {
            alert(`Error: ${data.error}`);
            return;
        }
        
        const confidence = (data.confidence * 100).toFixed(1);
        const polarity = data.polarity;
        const subjectivity = data.subjectivity;
        
        // Color based on sentiment
        let color = '#6b7280'; // neutral gray
        if (data.sentiment === 'Positive') color = '#10b981'; // green
        if (data.sentiment === 'Negative') color = '#ef4444'; // red
        
        let html = `
            <h3 style="color: ${color}">${data.emoji} Sentiment: ${data.sentiment}</h3>
            <p><strong>Confidence:</strong> ${confidence}%</p>
            <div class="confidence-bar">
                <div class="confidence-fill" style="width: ${confidence}%; background: ${color}"></div>
            </div>
            <div style="margin-top: 1rem;">
                <p><strong>Polarity:</strong> ${polarity} <span style="font-size: 0.9em; color: #6b7280;">(${polarity > 0 ? 'positive' : polarity < 0 ? 'negative' : 'neutral'})</span></p>
                <p><strong>Subjectivity:</strong> ${subjectivity} <span style="font-size: 0.9em; color: #6b7280;">(${subjectivity > 0.5 ? 'subjective' : 'objective'})</span></p>
            </div>
        `;
        
        if (data.analysis_text && data.language !== 'en') {
            html += `<p style="margin-top: 1rem; font-size: 0.9em; color: #6b7280;"><em>Analyzed in English: "${data.analysis_text}"</em></p>`;
        }
        
        document.getElementById('sentimentResult').innerHTML = html;
        document.getElementById('sentimentResult').classList.remove('hidden');
    } catch (error) {
        console.error('Error:', error);
        alert('Sentiment analysis failed. Please try again.');
    }
}

function swapLanguages() {
    const fromLang = document.getElementById('fromLang');
    const toLang = document.getElementById('toLang');
    [fromLang.value, toLang.value] = [toLang.value, fromLang.value];
}

async function translateText() {
    const text = document.getElementById('translationText').value.trim();
    if (!text) return alert('Please enter text to translate');

    const fromLang = document.getElementById('fromLang').value;
    const toLang = document.getElementById('toLang').value;

    if (fromLang === toLang) {
        return alert('Source and target languages must be different!');
    }

    try {
        const response = await fetch('/translate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, from: fromLang, to: toLang })
        });

        const data = await response.json();
        
        if (data.error) {
            alert(`Translation error: ${data.error}`);
            return;
        }
        
        document.getElementById('translationResult').innerHTML = `
            <h3>Translation</h3>
            <p>${data.translation}</p>
        `;
        document.getElementById('translationResult').classList.remove('hidden');
    } catch (error) {
        console.error('Error:', error);
        alert('Translation failed. Please try again.');
    }
}
