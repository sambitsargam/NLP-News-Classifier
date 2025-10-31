import React, { useState, useEffect } from 'react';
import './App.css';
import PredictionForm from './components/PredictionForm';
import ResultDisplay from './components/ResultDisplay';
import { newsAPI } from './api';

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [modelInfo, setModelInfo] = useState(null);

  useEffect(() => {
    // Check health and load model info on component mount
    const initApp = async () => {
      try {
        const health = await newsAPI.healthCheck();
        if (!health.model_loaded) {
          setError('Model not loaded. Please ensure the backend is running and model is trained.');
        }

        const info = await newsAPI.getModelInfo();
        setModelInfo(info);
      } catch (error) {
        setError('Failed to connect to backend. Make sure the server is running on http://localhost:8000');
        console.error('Initialization error:', error);
      }
    };

    initApp();
  }, []);

  const handlePredict = async (text, modelType) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const prediction = await newsAPI.predict(text, modelType);
      setResult(prediction);
    } catch (error) {
      setError(error.message || 'Failed to classify article');
      setResult({ error: error.message || 'Classification failed' });
      console.error('Prediction error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1>📰 News Category Classifier</h1>
          <p>Automatically classify news articles into categories using AI</p>
          {modelInfo && (
            <div className="model-stats">
              <span>Categories: {modelInfo.total_categories}</span>
              <span>•</span>
              <span>Model: {modelInfo.sklearn_model_loaded ? '✓ Loaded' : 'Loading...'}</span>
            </div>
          )}
        </div>
      </header>

      <main className="app-main">
        <div className="container">
          {error && (
            <div className="app-error">
              <p>⚠️ {error}</p>
            </div>
          )}

          <PredictionForm onPredict={handlePredict} loading={loading} />
          <ResultDisplay result={result} loading={loading} />

          <section className="features-section">
            <div className="features-grid">
              <div className="feature-card">
                <div className="feature-icon">🚀</div>
                <h3>Fast & Accurate</h3>
                <p>Uses machine learning to quickly classify news into 7+ categories</p>
              </div>

              <div className="feature-card">
                <div className="feature-icon">📊</div>
                <h3>Confidence Scores</h3>
                <p>See prediction confidence for each category</p>
              </div>

              <div className="feature-card">
                <div className="feature-icon">📁</div>
                <h3>File Upload</h3>
                <p>Upload text files directly for classification</p>
              </div>

              <div className="feature-card">
                <div className="feature-icon">⚙️</div>
                <h3>Multiple Models</h3>
                <p>Choose between fast Sklearn or accurate Transformer models</p>
              </div>
            </div>
          </section>

          <section className="info-section">
            <h2>About This Classifier</h2>
            <div className="info-content">
              <div className="info-item">
                <h4>🎯 How It Works</h4>
                <p>
                  The classifier uses Natural Language Processing (NLP) to analyze the text of news articles.
                  It extracts features from the text and uses machine learning models to predict the most
                  appropriate category. The system provides confidence scores for transparency.
                </p>
              </div>

              <div className="info-item">
                <h4>📂 Supported Categories (12)</h4>
                <div className="categories-grid">
                  <span className="category-badge">💼 Business</span>
                  <span className="category-badge">🎓 Education</span>
                  <span className="category-badge">🎬 Entertainment</span>
                  <span className="category-badge">💰 Finance</span>
                  <span className="category-badge">🏥 Health</span>
                  <span className="category-badge">⚖️ Legal</span>
                  <span className="category-badge">🎨 Lifestyle</span>
                  <span className="category-badge">🏛️ Politics</span>
                  <span className="category-badge">🔬 Science</span>
                  <span className="category-badge">⚽ Sports</span>
                  <span className="category-badge">💻 Technology</span>
                  <span className="category-badge">🌍 World</span>
                </div>
              </div>

              <div className="info-item">
                <h4>🔧 Available Models</h4>
                <p>
                  <strong>Sklearn:</strong> Fast TF-IDF + Naive Bayes model, ideal for quick classifications.
                  <br />
                  <strong>Transformer:</strong> Advanced BART model for more nuanced classification.
                </p>
              </div>
            </div>
          </section>
        </div>
      </main>

      <footer className="app-footer">
        <p>© 2024 News Category Classifier • Powered by NLP & Machine Learning</p>
      </footer>
    </div>
  );
}

export default App;
