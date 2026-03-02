/**
 * Frontend JavaScript for Tamil Text Normalization
 * Handles user interactions and API communication
 */

// Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// DOM Elements
const normalizeBtn = document.getElementById('normalize-btn');
const inputText = document.getElementById('input-text');
const outputSection = document.getElementById('output-section');
const errorSection = document.getElementById('error-section');
const normalizedTextEl = document.getElementById('normalized-text');
const ssmlOutputEl = document.getElementById('ssml-output');
const dfaInfoEl = document.getElementById('dfa-info');
const errorMessageEl = document.getElementById('error-message');
const copySsmlBtn = document.getElementById('copy-ssml-btn');

/**
 * Get selected categories from all checkboxes
 * Dynamically collects any checkbox whose id starts with "category-"
 */
function getSelectedCategories() {
    const checkboxes = document.querySelectorAll('input[type="checkbox"][id^="category-"]');
    const categories = [];
    checkboxes.forEach(cb => {
        if (cb.checked) categories.push(cb.value);
    });
    return categories;
}

/**
 * Show error message
 */
function showError(message) {
    errorSection.style.display = 'block';
    outputSection.style.display = 'none';
    errorMessageEl.textContent = message;
    errorSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

/**
 * Hide error message
 */
function hideError() {
    errorSection.style.display = 'none';
}

/**
 * Display DFA state transitions
 */
function displayDFAInfo(dfaInfo) {
    if (!dfaInfo || dfaInfo.length === 0) {
        dfaInfoEl.innerHTML = '<p style="color: var(--text-muted);">No DFA transitions detected</p>';
        return;
    }

    let html = '';
    dfaInfo.forEach(item => {
        html += `
            <div class="dfa-item">
                <div class="dfa-category">${item.category}</div>
                <div class="dfa-original">Original: <strong>${item.original}</strong></div>
                <div class="dfa-states">
                    ${item.states.map((state, index) => {
            if (index === item.states.length - 1) {
                return `<span class="dfa-state">${state}</span>`;
            }
            return `<span class="dfa-state">${state}</span><span class="dfa-arrow">→</span>`;
        }).join('')}
                </div>
            </div>
        `;
    });

    dfaInfoEl.innerHTML = html;
}

/**
 * Call normalization API
 */
async function normalizeText() {
    const text = inputText.value.trim();

    if (!text) {
        showError('இயல்பாக்கம் செய்ய உரையை உள்ளிடவும்');
        return;
    }

    const categories = getSelectedCategories();
    if (categories.length === 0) {
        showError('குறைந்தது ஒரு இயல்பாக்க வகையைத் தேர்வு செய்யவும்');
        return;
    }

    hideError();
    normalizeBtn.disabled = true;
    normalizeBtn.innerHTML = '<span class="btn-icon">⏳</span> Processing...';

    try {
        const response = await fetch(`${API_BASE_URL}/normalize`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text,
                categories: categories,
                language: document.getElementById('language').value
            })
        });

        const data = await response.json();

        if (!response.ok || !data.success) {
            throw new Error(data.error || 'இயல்பாக்கம் தோல்வியடைந்தது');
        }

        normalizedTextEl.textContent = data.normalized_text;
        ssmlOutputEl.textContent = data.ssml;
        displayDFAInfo(data.dfa_info);

        outputSection.style.display = 'block';
        outputSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

    } catch (error) {
        console.error('Error:', error);
        showError(`பிழை: ${error.message}. backend சேவை இயங்குகிறதா என்பதை உறுதிப்படுத்தவும்.`);
    } finally {
        normalizeBtn.disabled = false;
        normalizeBtn.innerHTML = '<span class="btn-icon">⚡</span> Generate Normalization';
    }
}

/**
 * Copy SSML to clipboard
 */
async function copySsmlToClipboard() {
    const ssmlText = ssmlOutputEl.textContent;

    try {
        await navigator.clipboard.writeText(ssmlText);

        const originalText = copySsmlBtn.textContent;
        copySsmlBtn.textContent = '✓ Copied!';
        copySsmlBtn.style.background = 'var(--success-gradient)';

        setTimeout(() => {
            copySsmlBtn.textContent = originalText;
            copySsmlBtn.style.background = '';
        }, 2000);

    } catch (error) {
        console.error('Failed to copy:', error);
        alert('SSML ஐ கிளிப்போர்டுக்கு நகலெடுக்க முடியவில்லை');
    }
}

/**
 * Check backend health on page load
 */
async function checkBackendHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();

        if (data.status === 'healthy') {
            console.log('✓ Backend is healthy:', data);
        }
    } catch (error) {
        console.warn('⚠ Backend க்கு அணுக முடியவில்லை. backend சேவையை தொடங்கவும்.');
        showError('Backend சேவை இயங்கவில்லை. இதை தொடங்க: python backend/app.py');
    }
}

// Event Listeners
normalizeBtn.addEventListener('click', normalizeText);
copySsmlBtn.addEventListener('click', copySsmlToClipboard);

inputText.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key === 'Enter') {
        normalizeText();
    }
});

window.addEventListener('DOMContentLoaded', checkBackendHealth);

console.log('💡 குறிப்பு: உரையை விரைவாக இயல்பாக்குவதற்கு Ctrl+Enter ஐ பயன்படுத்தவும்');
