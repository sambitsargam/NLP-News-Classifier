import React, { useState } from 'react';
import './PredictionForm.css';
import { FiSend, FiFile, FiLink } from 'react-icons/fi';

export default function PredictionForm({ onPredict, loading }) {
  const [text, setText] = useState('');
  const [url, setUrl] = useState('');
  const [modelType, setModelType] = useState('sklearn');
  const [activeTab, setActiveTab] = useState('text');
  const [fetchingUrl, setFetchingUrl] = useState(false);

  const handleTextPredict = () => {
    if (text.trim()) {
      onPredict(text, modelType);
    }
  };

  const handleFetchUrl = async () => {
    if (!url.trim()) {
      alert('Please enter a URL');
      return;
    }

    setFetchingUrl(true);
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`Failed to fetch URL: ${response.status}`);
      }

      const html = await response.text();
      
      // Extract text from HTML
      const parser = new DOMParser();
      const doc = parser.parseFromString(html, 'text/html');
      
      // Remove script and style elements
      doc.querySelectorAll('script, style').forEach(el => el.remove());
      
      // Get text content
      let extractedText = doc.body.innerText
        .split('\n')
        .map(line => line.trim())
        .filter(line => line.length > 0)
        .join('\n');

      // Clean up excessive newlines
      extractedText = extractedText.replace(/\n\n+/g, '\n\n').trim();

      if (extractedText) {
        setText(extractedText);
        setActiveTab('text');
        alert(`Extracted ${extractedText.length} characters from the URL`);
      } else {
        alert('No text content found on the page');
      }
    } catch (error) {
      alert(`Error fetching URL: ${error.message}`);
    } finally {
      setFetchingUrl(false);
    }
  };

  const handleFileUpload = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        setText(event.target.result);
        setActiveTab('text');
      };
      reader.readAsText(file);
    }
  };

  const handlePaste = async () => {
    try {
      const clipboardText = await navigator.clipboard.readText();
      setText(clipboardText);
    } catch (error) {
      alert('Failed to read clipboard');
    }
  };

  return (
    <div className="prediction-form">
      <div className="form-header">
        <h2>📰 News Article Classifier</h2>
        <p>Paste, upload, or fetch your news article to classify it</p>
      </div>

      <div className="form-tabs">
        <button
          className={`tab ${activeTab === 'text' ? 'active' : ''}`}
          onClick={() => setActiveTab('text')}
        >
          ✏️ Text Input
        </button>
        <button
          className={`tab ${activeTab === 'file' ? 'active' : ''}`}
          onClick={() => setActiveTab('file')}
        >
          📁 Upload File
        </button>
        <button
          className={`tab ${activeTab === 'url' ? 'active' : ''}`}
          onClick={() => setActiveTab('url')}
        >
          🔗 From URL
        </button>
      </div>

      <div className="form-content">
        {activeTab === 'text' ? (
          <div className="text-input-section">
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Enter or paste your news article here..."
              className="article-textarea"
              disabled={loading}
            />
            <div className="textarea-footer">
              <span className="char-count">{text.length} characters</span>
              <button
                onClick={handlePaste}
                className="paste-btn"
                disabled={loading}
              >
                📋 Paste from Clipboard
              </button>
            </div>
          </div>
        ) : activeTab === 'file' ? (
          <div className="file-input-section">
            <label className="file-input-label">
              <div className="file-input-box">
                <FiFile size={48} />
                <p>Click to select a file or drag and drop</p>
                <p className="file-hint">Supported: .txt files</p>
              </div>
              <input
                type="file"
                accept=".txt"
                onChange={handleFileUpload}
                className="hidden-file-input"
                disabled={loading}
              />
            </label>
          </div>
        ) : (
          <div className="url-input-section">
            <div className="url-input-group">
              <FiLink className="url-icon" />
              <input
                type="url"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="Enter article URL (e.g., https://example.com/article)"
                className="url-input"
                disabled={loading || fetchingUrl}
              />
            </div>
            <button
              onClick={handleFetchUrl}
              disabled={!url.trim() || loading || fetchingUrl}
              className="fetch-url-btn"
            >
              {fetchingUrl ? (
                <>
                  <span className="spinner"></span>
                  Fetching...
                </>
              ) : (
                <>
                  🌐 Fetch Article Text
                </>
              )}
            </button>
            <p className="url-hint">
              The system will extract text content from the webpage and load it above.
            </p>
          </div>
        )}
      </div>

      <div className="model-selection">
        <label htmlFor="model-type">🤖 Model Type:</label>
        <select
          id="model-type"
          value={modelType}
          onChange={(e) => setModelType(e.target.value)}
          disabled={loading}
          className="model-select"
        >
          <option value="sklearn">Sklearn (Fast & Reliable)</option>
          <option value="transformer">Transformer (Advanced)</option>
        </select>
      </div>

      <button
        onClick={handleTextPredict}
        disabled={!text.trim() || loading}
        className="predict-btn"
      >
        {loading ? (
          <>
            <span className="spinner"></span>
            Classifying...
          </>
        ) : (
          <>
            <FiSend /> Classify Article
          </>
        )}
      </button>
    </div>
  );
}
