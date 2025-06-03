function showTab(event, tabName) {
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
}

const languageNames = {
    en: 'English', zh: 'Chinese', ja: 'Japanese'
};

async function detectLanguage() {
    const text = document.getElementById('languageText').value.trim();
    if (!text) return alert('Please enter text to analyze');

    await new Promise(resolve => setTimeout(resolve, 1500)); // Simulate API

    let detected = 'en', confidence = 0.95;
    if (/[\u4e00-\u9fff]/.test(text)) { detected = 'zh'; confidence = 0.98; }
    else if (/[\u3040-\u30ff]/.test(text)) { detected = 'ja'; confidence = 0.97; }

    document.getElementById('languageResult').innerHTML = `
        <h3>Detected Language: ${languageNames[detected]}</h3>
        <p>Confidence: ${(confidence * 100).toFixed(1)}%</p>
    `;
    document.getElementById('languageResult').classList.remove('hidden');
}

async function analyzeSentiment() {
    const text = document.getElementById('sentimentText').value.trim();
    if (!text) return alert('Please enter text to analyze');

    await new Promise(resolve => setTimeout(resolve, 1500));

    let label = 'NEUTRAL';
    if (text.includes('good')) label = 'POSITIVE';
    if (text.includes('bad')) label = 'NEGATIVE';

    document.getElementById('sentimentResult').innerHTML = `
        <h3>Sentiment: ${label}</h3>
        <p>Confidence: ${(Math.random() * 20 + 80).toFixed(1)}%</p>
    `;
    document.getElementById('sentimentResult').classList.remove('hidden');
}

function swapLanguages() {
    const fromLang = document.getElementById('fromLang');
    const toLang = document.getElementById('toLang');
    [fromLang.value, toLang.value] = [toLang.value, fromLang.value];
}

async function translateText() {
    const text = document.getElementById('translationText').value.trim();
    if (!text) return alert('Please enter text to translate');

    await new Promise(resolve => setTimeout(resolve, 1500));

    const translation = `[Translated Text] ${text}`;
    document.getElementById('translationResult').innerText = translation;
    document.getElementById('translationResult').classList.remove('hidden');
}
