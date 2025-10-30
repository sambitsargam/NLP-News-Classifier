import React, { useState } from 'react';
import './PredictionForm.css';
import { FiSend, FiFile } from 'react-icons/fi';

export default function PredictionForm({ onPredict, loading }) {
  const [text, setText] = useState('');
  const [modelType, setModelType] = useState('sklearn');
  const [activeTab, setActiveTab] = useState('text');

  const handleTextPredict = () => {
    if (text.trim()) {
      onPredict(text, modelType);
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
        <h2>📰 Enter News Article</h2>
        <p>Paste or upload your news article to classify it</p>
      </div>

      <div className="form-tabs">
        <button
          className={`tab ${activeTab === 'text' ? 'active' : ''}`}
          onClick={() => setActiveTab('text')}
        >
          Text Input
        </button>
        <button
          className={`tab ${activeTab === 'file' ? 'active' : ''}`}
          onClick={() => setActiveTab('file')}
        >
          Upload File
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
                📋 Paste
              </button>
            </div>
          </div>
        ) : (
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
        )}
      </div>

      <div className="model-selection">
        <label htmlFor="model-type">Model Type:</label>
        <select
          id="model-type"
          value={modelType}
          onChange={(e) => setModelType(e.target.value)}
          disabled={loading}
          className="model-select"
        >
          <option value="sklearn">Sklearn (Fast)</option>
          <option value="transformer">Transformer (Accurate)</option>
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
