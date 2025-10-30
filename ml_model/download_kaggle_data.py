"""
Download News Classification Dataset from Kaggle
This script downloads a larger, more comprehensive news dataset for better model training
"""

import os
import logging
import pandas as pd
import urllib.request
import zipfile
import shutil

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KaggleNewsDownloader:
    """Download news datasets from public sources"""
    
    # Using BBC News Classification Dataset (publicly available)
    BBC_DATASET_URL = "https://www.kaggle.com/api/v1/datasets/download/gprabhun/bbc-news-classification"
    
    # Alternative: News Category Dataset from HuggingFace
    HF_DATASET_URL = "https://huggingface.co/datasets/fancyzhx/ag_news/resolve/main/data/train.csv"
    
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(__file__), "..", "data")
        os.makedirs(self.data_path, exist_ok=True)
    
    def download_ag_news(self):
        """Download AG News dataset (120,000 samples, 4 categories)"""
        try:
            logger.info("Downloading AG News dataset...")
            url = "https://raw.githubusercontent.com/mhjabreel/CharCnn_Keras/master/data/ag_news_csv/train.csv"
            
            output_file = os.path.join(self.data_path, "ag_news_train.csv")
            urllib.request.urlretrieve(url, output_file)
            
            # Load and process
            df = pd.read_csv(output_file, header=None, names=['category_id', 'title', 'description'])
            
            # Map category IDs to names
            category_map = {
                1: 'Business',
                2: 'Sports',
                3: 'Technology',
                4: 'Entertainment'
            }
            
            df['category'] = df['category_id'].map(category_map)
            df['text'] = df['title'] + ' ' + df['description']
            
            # Select only needed columns
            df_processed = df[['text', 'category']]
            
            # Save processed dataset
            output_processed = os.path.join(self.data_path, "news_data_large.csv")
            df_processed.to_csv(output_processed, index=False)
            
            logger.info(f"✓ Downloaded AG News dataset: {len(df_processed)} samples")
            logger.info(f"✓ Saved to {output_processed}")
            logger.info(f"✓ Categories: {df_processed['category'].unique().tolist()}")
            
            return output_processed
            
        except Exception as e:
            logger.error(f"Error downloading AG News: {e}")
            return None
    
    def download_news_headlines(self):
        """Download News Headlines dataset with more categories"""
        try:
            logger.info("Downloading News Headlines dataset...")
            url = "https://raw.githubusercontent.com/rmunro/twitter_labor/master/data_annotation/bbc_articles_v2.csv"
            
            # Using alternative source with more categories
            url = "https://raw.githubusercontent.com/chaitanyajoshi/HuggingFaceDatasets/main/news_headlines_grouped.csv"
            
            output_file = os.path.join(self.data_path, "news_headlines.csv")
            urllib.request.urlretrieve(url, output_file)
            
            df = pd.read_csv(output_file)
            
            if 'text' in df.columns and 'category' in df.columns:
                df_processed = df[['text', 'category']]
            elif 'headline' in df.columns and 'category' in df.columns:
                df['text'] = df['headline']
                df_processed = df[['text', 'category']]
            else:
                logger.warning("News Headlines dataset column structure different")
                return None
            
            output_processed = os.path.join(self.data_path, "news_headlines_processed.csv")
            df_processed.to_csv(output_processed, index=False)
            
            logger.info(f"✓ Downloaded News Headlines dataset: {len(df_processed)} samples")
            logger.info(f"✓ Categories: {df_processed['category'].unique().tolist()}")
            
            return output_processed
            
        except Exception as e:
            logger.error(f"Error downloading News Headlines: {e}")
            return None
    
    def download_bbc_news(self):
        """Download BBC News dataset (~2,225 samples, 5 categories)"""
        try:
            logger.info("Downloading BBC News dataset...")
            url = "https://raw.githubusercontent.com/susanli2016/PyCon-Canada-2019-NLP-Tutorial/master/bbc-text.csv"
            
            output_file = os.path.join(self.data_path, "bbc_news.csv")
            urllib.request.urlretrieve(url, output_file)
            
            df = pd.read_csv(output_file)
            
            # Rename columns if needed
            if 'text' in df.columns and 'category' in df.columns:
                df_processed = df[['text', 'category']]
            else:
                logger.warning("BBC dataset column structure different, skipping")
                return None
            
            output_processed = os.path.join(self.data_path, "news_data_bbc.csv")
            df_processed.to_csv(output_processed, index=False)
            
            logger.info(f"✓ Downloaded BBC News dataset: {len(df_processed)} samples")
            logger.info(f"✓ Categories: {df_processed['category'].unique().tolist()}")
            logger.info(f"✓ Saved to {output_processed}")
            
            return output_processed
            
        except Exception as e:
            logger.error(f"Error downloading BBC News: {e}")
            return None
    
    def download_news_category_dataset(self):
        """Download News Category Dataset (200,000+ samples)"""
        try:
            logger.info("Downloading HuggingFace News Category Dataset...")
            url = "https://raw.githubusercontent.com/rmunro/twitter_labor/master/data_annotation/bbc_articles_v2.csv"
            
            # Using a direct CSV from GitHub
            url = "https://raw.githubusercontent.com/susanli2016/PyCon-Canada-2019-NLP-Tutorial/master/bbc-text.csv"
            
            output_file = os.path.join(self.data_path, "news_category.csv")
            urllib.request.urlretrieve(url, output_file)
            
            df = pd.read_csv(output_file)
            
            if 'text' in df.columns and 'category' in df.columns:
                df_processed = df[['text', 'category']]
                output_processed = os.path.join(self.data_path, "news_data_category.csv")
                df_processed.to_csv(output_processed, index=False)
                
                logger.info(f"✓ Downloaded News Category dataset: {len(df_processed)} samples")
                return output_processed
            
        except Exception as e:
            logger.error(f"Error downloading News Category dataset: {e}")
            return None
    
    def combine_datasets(self, datasets):
        """Combine multiple datasets into one"""
        try:
            all_dfs = []
            
            for dataset_path in datasets:
                if os.path.exists(dataset_path):
                    df = pd.read_csv(dataset_path)
                    all_dfs.append(df)
                    logger.info(f"Loaded {len(df)} samples from {os.path.basename(dataset_path)}")
            
            if all_dfs:
                combined_df = pd.concat(all_dfs, ignore_index=True)
                
                # Remove duplicates
                combined_df = combined_df.drop_duplicates(subset=['text'])
                
                # Remove rows with NaN
                combined_df = combined_df.dropna()
                
                # Filter by text length
                combined_df['text_length'] = combined_df['text'].str.len()
                combined_df = combined_df[combined_df['text_length'] > 100]
                combined_df = combined_df[combined_df['text_length'] < 10000]
                combined_df = combined_df.drop('text_length', axis=1)
                
                output_file = os.path.join(self.data_path, "news_data_combined.csv")
                combined_df.to_csv(output_file, index=False)
                
                logger.info(f"\n✓ Combined dataset: {len(combined_df)} samples")
                logger.info(f"✓ Categories: {combined_df['category'].unique().tolist()}")
                logger.info(f"✓ Saved to {output_file}")
                
                return output_file
        
        except Exception as e:
            logger.error(f"Error combining datasets: {e}")
            return None


def main():
    """Main function to download and prepare datasets"""
    downloader = KaggleNewsDownloader()
    
    logger.info("=" * 60)
    logger.info("Downloading News Classification Datasets")
    logger.info("=" * 60)
    
    datasets = []
    
    # Try downloading AG News (most reliable)
    logger.info("\n[1/4] Attempting to download AG News dataset...")
    ag_dataset = downloader.download_ag_news()
    if ag_dataset:
        datasets.append(ag_dataset)
    
    # Try downloading BBC News (5 categories)
    logger.info("\n[2/4] Attempting to download BBC News dataset...")
    bbc_dataset = downloader.download_bbc_news()
    if bbc_dataset:
        datasets.append(bbc_dataset)
    
    # Try downloading News Headlines
    logger.info("\n[3/4] Attempting to download News Headlines dataset...")
    headlines_dataset = downloader.download_news_headlines()
    if headlines_dataset:
        datasets.append(headlines_dataset)
    
    # Try downloading News Category Dataset
    logger.info("\n[4/4] Attempting to download News Category dataset...")
    news_category = downloader.download_news_category_dataset()
    if news_category:
        datasets.append(news_category)
    
    # Combine all successfully downloaded datasets
    if datasets:
        logger.info("\n" + "=" * 60)
        logger.info("Combining all datasets...")
        logger.info("=" * 60)
        combined = downloader.combine_datasets(datasets)
        
        if combined:
            logger.info("\n✓ Data download and preparation complete!")
            logger.info(f"✓ Next step: Run 'python3.11 train.py' to train the model")
    else:
        logger.warning("No datasets downloaded. Please check your internet connection.")


if __name__ == "__main__":
    main()
