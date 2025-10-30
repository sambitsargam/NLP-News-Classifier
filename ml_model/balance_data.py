"""
Balance and clean the dataset for training
"""

import os
import pandas as pd
import logging
from sklearn.utils import shuffle

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def balance_dataset():
    """Balance dataset across all categories"""
    
    data_path = os.path.join(os.path.dirname(__file__), "..", "data")
    combined_file = os.path.join(data_path, "news_data_combined.csv")
    
    # Load data
    df = pd.read_csv(combined_file)
    logger.info(f"Original dataset: {len(df)} samples, {df['category'].nunique()} categories")
    
    # Check category distribution
    logger.info(f"\nOriginal category distribution:")
    logger.info(df['category'].value_counts())
    
    # Remove duplicates
    df = df.drop_duplicates(subset=['text'])
    logger.info(f"\nAfter removing duplicates: {len(df)} samples")
    
    # Remove NaN
    df = df.dropna()
    
    # Balance: take minimum samples from underrepresented categories and sample from larger ones
    min_samples = 5000  # Minimum samples per category
    max_samples = 30000  # Maximum samples per category
    
    balanced_dfs = []
    
    for category in df['category'].unique():
        cat_df = df[df['category'] == category].copy()
        
        if len(cat_df) < min_samples:
            # Use all samples and add more synthetic variations
            logger.warning(f"Category '{category}' has only {len(cat_df)} samples (less than {min_samples})")
            # Keep as is
            balanced_dfs.append(cat_df)
        elif len(cat_df) > max_samples:
            # Sample randomly
            balanced_dfs.append(cat_df.sample(n=max_samples, random_state=42))
        else:
            balanced_dfs.append(cat_df)
    
    # Combine
    balanced_df = pd.concat(balanced_dfs, ignore_index=True)
    
    # Shuffle
    balanced_df = shuffle(balanced_df, random_state=42)
    
    # Save
    output_file = os.path.join(data_path, "news_data_combined.csv")
    balanced_df.to_csv(output_file, index=False)
    
    logger.info(f"\n{'='*60}")
    logger.info(f"Balanced dataset: {len(balanced_df)} samples")
    logger.info(f"Total categories: {balanced_df['category'].nunique()}")
    logger.info(f"Categories: {sorted(balanced_df['category'].unique().tolist())}")
    logger.info(f"{'='*60}")
    logger.info(f"Balanced category distribution:")
    logger.info(balanced_df['category'].value_counts())
    logger.info(f"✓ Saved to {output_file}")
    
    return balanced_df


if __name__ == "__main__":
    balance_dataset()
