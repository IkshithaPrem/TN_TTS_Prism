import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [text, setText] = useState('');
  const [locale, setLocale] = useState('hi-IN');
  const [normalizedText, setNormalizedText] = useState('');
  const [ssml, setSsml] = useState('');
  const [tokens, setTokens] = useState([]);
  const [locales, setLocales] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showRules, setShowRules] = useState(false);
  const [rules, setRules] = useState(null);

  useEffect(() => {
    fetchLocales();
  }, []);

  const fetchLocales = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/locales`);
      setLocales(response.data.locales);
    } catch (err) {
      console.error('Error fetching locales:', err);
    }
  };

  const handleNormalize = async () => {
    if (!text.trim()) {
      setError('Please enter some text');
      return;
    }

    setLoading(true);
    setError('');
    
    try {
      // Normalize text
      const normalizeResponse = await axios.post(`${API_BASE_URL}/normalize`, {
        locale,
        text
      });
      
      setNormalizedText(normalizeResponse.data.normalized_text);
      setTokens(normalizeResponse.data.tokens || []);

      // Generate SSML
      const ssmlResponse = await axios.post(`${API_BASE_URL}/generate_ssml`, {
        locale,
        text,
        use_ssml: true
      });
      
      setSsml(ssmlResponse.data.ssml);
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred');
      console.error('Error normalizing text:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleExportRules = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/export_rules/${locale}`);
      setRules(response.data);
      setShowRules(true);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error exporting rules');
      console.error('Error exporting rules:', err);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    alert('Copied to clipboard!');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            Indian Language Text Normalization
          </h1>
          <p className="text-lg text-gray-600">
            Text Normalization + SSML Rule Generator for TTS
          </p>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          {/* Input Section */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-semibold text-gray-700 mb-4">Input</h2>
            
            {/* Locale Selector */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Select Locale
              </label>
              <select
                value={locale}
                onChange={(e) => setLocale(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              >
                {locales.map((loc) => (
                  <option key={loc} value={loc}>
                    {loc}
                  </option>
                ))}
              </select>
            </div>

            {/* Text Input */}
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Enter Text
              </label>
              <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Enter text to normalize (e.g., ₹250 on 12/03/2024 at 10:30AM)"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 h-32 resize-none"
              />
            </div>

            {/* Buttons */}
            <div className="flex gap-3">
              <button
                onClick={handleNormalize}
                disabled={loading}
                className="flex-1 bg-indigo-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {loading ? 'Normalizing...' : 'Normalize'}
              </button>
              <button
                onClick={handleExportRules}
                className="px-6 py-3 bg-gray-600 text-white rounded-lg font-semibold hover:bg-gray-700 transition-colors"
              >
                Export Rules
              </button>
            </div>

            {error && (
              <div className="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded-lg">
                {error}
              </div>
            )}
          </div>

          {/* Output Section */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-semibold text-gray-700 mb-4">Output</h2>
            
            {/* Normalized Text */}
            <div className="mb-4">
              <div className="flex justify-between items-center mb-2">
                <label className="block text-sm font-medium text-gray-700">
                  Normalized Text
                </label>
                {normalizedText && (
                  <button
                    onClick={() => copyToClipboard(normalizedText)}
                    className="text-sm text-indigo-600 hover:text-indigo-800"
                  >
                    Copy
                  </button>
                )}
              </div>
              <div className="w-full px-4 py-3 bg-gray-50 border border-gray-300 rounded-lg min-h-32">
                {normalizedText || <span className="text-gray-400">Normalized text will appear here...</span>}
              </div>
            </div>

            {/* SSML Output */}
            <div className="mb-4">
              <div className="flex justify-between items-center mb-2">
                <label className="block text-sm font-medium text-gray-700">
                  SSML Output
                </label>
                {ssml && (
                  <button
                    onClick={() => copyToClipboard(ssml)}
                    className="text-sm text-indigo-600 hover:text-indigo-800"
                  >
                    Copy
                  </button>
                )}
              </div>
              <pre className="w-full px-4 py-3 bg-gray-50 border border-gray-300 rounded-lg min-h-32 text-sm overflow-x-auto">
                {ssml || <span className="text-gray-400">SSML will appear here...</span>}
              </pre>
            </div>
          </div>
        </div>

        {/* Tokens Section */}
        {tokens.length > 0 && (
          <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
            <h2 className="text-2xl font-semibold text-gray-700 mb-4">Normalized Tokens</h2>
            <div className="overflow-x-auto">
              <table className="w-full border-collapse">
                <thead>
                  <tr className="bg-gray-100">
                    <th className="border border-gray-300 px-4 py-2 text-left">Original</th>
                    <th className="border border-gray-300 px-4 py-2 text-left">Normalized</th>
                    <th className="border border-gray-300 px-4 py-2 text-left">Category</th>
                    <th className="border border-gray-300 px-4 py-2 text-left">Position</th>
                  </tr>
                </thead>
                <tbody>
                  {tokens.map((token, index) => (
                    <tr key={index} className="hover:bg-gray-50">
                      <td className="border border-gray-300 px-4 py-2">{token.original}</td>
                      <td className="border border-gray-300 px-4 py-2">{token.normalized}</td>
                      <td className="border border-gray-300 px-4 py-2">
                        <span className="px-2 py-1 bg-indigo-100 text-indigo-800 rounded text-sm">
                          {token.category}
                        </span>
                      </td>
                      <td className="border border-gray-300 px-4 py-2 text-sm text-gray-600">
                        {token.start}-{token.end}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Rules Viewer */}
        {showRules && rules && (
          <div className="bg-white rounded-lg shadow-lg p-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-2xl font-semibold text-gray-700">
                Rules for {rules.locale}
              </h2>
              <button
                onClick={() => setShowRules(false)}
                className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
              >
                Close
              </button>
            </div>
            <pre className="bg-gray-50 p-4 rounded-lg overflow-x-auto text-sm border border-gray-300">
              {JSON.stringify(rules.rules, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
