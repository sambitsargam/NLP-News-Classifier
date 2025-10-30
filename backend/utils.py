"""
Utility functions for text preprocessing and data handling
"""

import re
import logging
from typing import Dict, List
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

logger = logging.getLogger(__name__)

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
except Exception as e:
    logger.warning(f"Error downloading NLTK data: {e}")

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))


def preprocess_text(text: str) -> str:
    """
    Preprocess news article text for classification
    
    Steps:
    1. Convert to lowercase
    2. Remove URLs and HTML
    3. Remove special characters and punctuation
    4. Tokenize
    5. Remove stopwords
    6. Lemmatize
    
    Args:
        text: Raw text to preprocess
        
    Returns:
        Preprocessed text
    """
    try:
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove email addresses
        text = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '', text)
        
        # Remove special characters and numbers, keep only letters and spaces
        text = re.sub(r'[^a-z\s]', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords and lemmatize
        tokens = [
            lemmatizer.lemmatize(token)
            for token in tokens
            if token not in stop_words and len(token) > 2
        ]
        
        # Rejoin tokens
        processed_text = ' '.join(tokens)
        
        return processed_text if processed_text else text
        
    except Exception as e:
        logger.error(f"Text preprocessing error: {e}")
        return text


def generate_confidence_dict(predictions: list, categories: list) -> Dict[str, float]:
    """
    Generate a dictionary of confidence scores
    
    Args:
        predictions: Model prediction probabilities
        categories: List of category names
        
    Returns:
        Dictionary mapping categories to confidence scores
    """
    return {
        category: float(score)
        for category, score in zip(categories, predictions)
    }


def validate_text(text: str, min_length: int = 10, max_length: int = 100000) -> bool:
    """
    Validate input text
    
    Args:
        text: Text to validate
        min_length: Minimum text length
        max_length: Maximum text length
        
    Returns:
        True if valid, False otherwise
    """
    if not text or not isinstance(text, str):
        return False
    
    text_length = len(text.strip())
    return min_length <= text_length <= max_length


def extract_keywords(text: str, num_keywords: int = 5) -> List[str]:
    """
    Extract keywords from text
    
    Args:
        text: Input text
        num_keywords: Number of keywords to extract
        
    Returns:
        List of keywords
    """
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        
        vectorizer = TfidfVectorizer(max_features=num_keywords, stop_words='english')
        vectorizer.fit_transform([text])
        
        return vectorizer.get_feature_names_out().tolist()
    except Exception as e:
        logger.error(f"Keyword extraction error: {e}")
        return []


def clean_html(html_text: str) -> str:
    """
    Clean HTML content and extract text
    
    Args:
        html_text: HTML content
        
    Returns:
        Cleaned text
    """
    try:
        from html.parser import HTMLParser
        
        class MLStripper(HTMLParser):
            def __init__(self):
                super().__init__()
                self.reset()
                self.strict = False
                self.convert_charrefs = True
                self.text = []
            
            def handle_data(self, data):
                self.text.append(data)
            
            def get_data(self):
                return ''.join(self.text)
        
        stripper = MLStripper()
        stripper.feed(html_text)
        return stripper.get_data()
    except Exception as e:
        logger.error(f"HTML cleaning error: {e}")
        return html_text
