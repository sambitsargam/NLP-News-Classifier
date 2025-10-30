"""
Model Service for News Classification
Handles loading and inference with different model types
"""

import os
import logging
import time
import pickle
import numpy as np
from typing import Dict, Any, List
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

logger = logging.getLogger(__name__)


class NewsClassifierService:
    """Service for news classification with support for multiple models"""
    
    # Default categories
    CATEGORIES = [
        "Sports",
        "Politics",
        "Technology",
        "Entertainment",
        "Business",
        "Health",
        "Science"
    ]
    
    def __init__(self, model_path: str = None):
        """
        Initialize the classifier service
        
        Args:
            model_path: Path to the trained model directory
        """
        self.model_path = model_path or os.path.join(
            os.path.dirname(__file__),
            "..",
            "ml_model",
            "models"
        )
        
        self.sklearn_model = None
        self.vectorizer = None
        self.transformer_model = None
        self.tokenizer = None
        
        self._load_models()
    
    def _load_models(self):
        """Load available models"""
        try:
            # Load sklearn model
            self._load_sklearn_model()
            logger.info("Sklearn model loaded successfully")
        except Exception as e:
            logger.warning(f"Failed to load sklearn model: {e}")
        
        try:
            # Load transformer model (optional)
            self._load_transformer_model()
            logger.info("Transformer model loaded successfully")
        except Exception as e:
            logger.info(f"Transformer model not available: {e}")
    
    def _load_sklearn_model(self):
        """Load pre-trained sklearn model"""
        try:
            model_file = os.path.join(self.model_path, "sklearn_model.joblib")
            
            if os.path.exists(model_file):
                # Load the pipeline which contains both vectorizer and classifier
                pipeline = joblib.load(model_file)
                # Extract vectorizer and classifier from pipeline
                self.vectorizer = pipeline.named_steps.get('tfidf')
                self.sklearn_model = pipeline.named_steps.get('classifier')
                
                if self.vectorizer and self.sklearn_model:
                    logger.info("Sklearn model and vectorizer loaded from pipeline")
                else:
                    logger.info("Pre-trained models not found. Using default model.")
                    self._create_default_sklearn_model()
            else:
                # If models don't exist, create a simple default one
                logger.info("Pre-trained models not found. Using default model.")
                self._create_default_sklearn_model()
        except Exception as e:
            logger.error(f"Error loading sklearn model: {e}")
            raise
    
    def _create_default_sklearn_model(self):
        """Create a default sklearn model for demonstration"""
        # This is a placeholder - in production, you'd train on real data
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.sklearn_model = MultinomialNB()
        logger.warning("Using default model - not trained on real data")
    
    def _load_transformer_model(self):
        """Load transformer model (optional)"""
        try:
            from transformers import pipeline
            # Using a pre-trained zero-shot classification model
            self.transformer_model = pipeline(
                "zero-shot-classification",
                model="facebook/bart-large-mnli"
            )
            logger.info("Transformer model (BART) loaded successfully")
        except Exception as e:
            logger.warning(f"Could not load transformer model: {e}")
    
    def predict(self, text: str, model_type: str = "sklearn") -> Dict[str, Any]:
        """
        Predict the category of news text
        
        Args:
            text: Preprocessed news article text
            model_type: Type of model to use ("sklearn" or "transformer")
            
        Returns:
            Dictionary with prediction results
        """
        start_time = time.time()
        
        if model_type == "transformer" and self.transformer_model:
            result = self._predict_transformer(text)
        else:
            result = self._predict_sklearn(text)
        
        result["processing_time"] = time.time() - start_time
        return result
    
    def _predict_sklearn(self, text: str) -> Dict[str, Any]:
        """Predict using sklearn model"""
        if not self.sklearn_model or not self.vectorizer:
            raise ValueError("Sklearn model not initialized")
        
        try:
            # Vectorize the text
            text_vector = self.vectorizer.transform([text])
            
            # Get predictions
            prediction = self.sklearn_model.predict(text_vector)[0]
            probabilities = self.sklearn_model.predict_proba(text_vector)[0]
            
            # Create confidence scores dictionary
            confidence_scores = {
                self.CATEGORIES[i]: float(probabilities[i])
                for i in range(len(self.CATEGORIES))
            }
            
            # Sort by confidence
            sorted_scores = dict(sorted(
                confidence_scores.items(),
                key=lambda x: x[1],
                reverse=True
            ))
            
            return {
                "category": self.CATEGORIES[prediction] if isinstance(prediction, int) else prediction,
                "confidence": float(max(probabilities)),
                "confidence_scores": sorted_scores,
                "model_type": "sklearn"
            }
        except Exception as e:
            logger.error(f"Sklearn prediction error: {e}")
            raise
    
    def _predict_transformer(self, text: str) -> Dict[str, Any]:
        """Predict using transformer model"""
        try:
            result = self.transformer_model(text, self.CATEGORIES, multi_class=True)
            
            confidence_scores = {
                label: float(score)
                for label, score in zip(result['labels'], result['scores'])
            }
            
            return {
                "category": result['labels'][0],
                "confidence": float(result['scores'][0]),
                "confidence_scores": confidence_scores,
                "model_type": "transformer"
            }
        except Exception as e:
            logger.error(f"Transformer prediction error: {e}")
            # Fallback to sklearn if transformer fails
            return self._predict_sklearn(text)
    
    def get_categories(self) -> List[str]:
        """Get list of available categories"""
        return self.CATEGORIES
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about loaded models"""
        vectorizer_features = 0
        if self.vectorizer:
            try:
                vectorizer_features = self.vectorizer.get_feature_names_out().shape[0]
            except Exception:
                # Vectorizer not fitted yet
                vectorizer_features = 0
        
        return {
            "sklearn_model_loaded": self.sklearn_model is not None,
            "transformer_model_loaded": self.transformer_model is not None,
            "categories": self.CATEGORIES,
            "total_categories": len(self.CATEGORIES),
            "vectorizer_features": vectorizer_features
        }
    
    def train_model(self, texts: List[str], labels: List[int]):
        """
        Train the sklearn model on provided data
        
        Args:
            texts: List of training texts
            labels: List of corresponding labels (indices)
        """
        try:
            # Vectorize
            X = self.vectorizer.fit_transform(texts)
            
            # Train
            self.sklearn_model.fit(X, labels)
            
            # Save models
            os.makedirs(self.model_path, exist_ok=True)
            joblib.dump(self.sklearn_model, os.path.join(self.model_path, "sklearn_model.joblib"))
            joblib.dump(self.vectorizer, os.path.join(self.model_path, "vectorizer.joblib"))
            
            logger.info(f"Model trained and saved. Accuracy on training data: {self.sklearn_model.score(X, labels):.2f}")
        except Exception as e:
            logger.error(f"Model training error: {e}")
            raise
