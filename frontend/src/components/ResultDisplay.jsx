import React from 'react';
import './ResultDisplay.css';
import { FiCheck, FiBarChart2 } from 'react-icons/fi';

export default function ResultDisplay({ result, loading }) {
  if (loading) {
    return null;
  }

  if (!result) {
    return null;
  }

  if (result.error) {
    return (
      <div className="result-container error">
        <div className="error-message">
          <p>❌ {result.error}</p>
        </div>
      </div>
    );
  }

  const confidencePercentage = (result.confidence * 100).toFixed(2);
  const maxConfidence = Math.max(...Object.values(result.confidence_scores));

  return (
    <div className="result-container">
      <div className="result-header">
        <h2>📊 Classification Result</h2>
      </div>

      <div className="result-main">
        <div className="result-category">
          <div className="category-icon">
            <FiCheck />
          </div>
          <div className="category-info">
            <p className="category-label">Predicted Category</p>
            <h3 className="category-name">{result.category}</h3>
            <p className="category-confidence">
              Confidence: <span className="confidence-value">{confidencePercentage}%</span>
            </p>
          </div>
        </div>

        <div className="confidence-bar">
          <div className="bar-fill" style={{ width: `${result.confidence * 100}%` }}></div>
        </div>
      </div>

      <div className="result-breakdown">
        <h4><FiBarChart2 /> Confidence Scores by Category</h4>
        <div className="scores-grid">
          {Object.entries(result.confidence_scores).map(([category, score]) => (
            <div key={category} className="score-item">
              <div className="score-header">
                <span className="score-category">{category}</span>
                <span className="score-value">{(score * 100).toFixed(1)}%</span>
              </div>
              <div className="score-bar">
                <div
                  className={`score-bar-fill ${score === maxConfidence ? 'highest' : ''}`}
                  style={{ width: `${score * 100}%` }}
                ></div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="result-metadata">
        <p className="processing-time">
          ⏱️ Processing Time: {result.processing_time?.toFixed(3)}s
        </p>
        <p className="article-preview">
          <strong>Article Preview:</strong> {result.input_text}
        </p>
      </div>
    </div>
  );
}
