"""
Preprocess and normalize news data
"""

import os
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def normalize_categories(df):
    """Normalize category names to standard format"""
    
    category_mapping = {
        'technology': 'Technology',
        'tech': 'Technology',
        'entertainment': 'Entertainment',
        'sports': 'Sports',
        'sport': 'Sports',
        'business': 'Business',
        'politics': 'Politics',
        'political': 'Politics',
        'health': 'Health',
        'science': 'Science',
        'world': 'World',
        'lifestyle': 'Lifestyle',
    }
    
    # Convert to lowercase, then map to standard category
    df['category_normalized'] = df['category'].str.lower().map(
        lambda x: category_mapping.get(x, x.title())
    )
    
    return df


def clean_text(text):
    """Clean text data"""
    if pd.isna(text):
        return ""
    
    text = str(text).strip()
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text


def preprocess_combined_data():
    """Preprocess and normalize the combined dataset"""
    
    data_path = os.path.join(os.path.dirname(__file__), "..", "data")
    combined_file = os.path.join(data_path, "news_data_combined.csv")
    
    logger.info(f"Loading combined dataset from {combined_file}")
    df = pd.read_csv(combined_file)
    
    logger.info(f"Original dataset shape: {df.shape}")
    logger.info(f"Original categories: {df['category'].unique().tolist()}")
    
    # Clean text
    df['text'] = df['text'].apply(clean_text)
    
    # Normalize categories
    df = normalize_categories(df)
    
    logger.info(f"Normalized categories: {df['category_normalized'].unique().tolist()}")
    
    # Remove rows with empty text
    df = df[df['text'].str.len() > 0]
    
    # Remove duplicates
    df = df.drop_duplicates(subset=['text'])
    
    # Use normalized categories
    df['category'] = df['category_normalized']
    df = df[['text', 'category']]
    
    logger.info(f"Cleaned dataset shape: {df.shape}")
    logger.info(f"Final categories: {df['category'].unique().tolist()}")
    logger.info(f"Category distribution:\n{df['category'].value_counts()}")
    
    # Save cleaned data
    output_file = os.path.join(data_path, "news_data_combined.csv")
    df.to_csv(output_file, index=False)
    logger.info(f"✓ Saved cleaned data to {output_file}")
    
    return df


if __name__ == "__main__":
    preprocess_combined_data()
