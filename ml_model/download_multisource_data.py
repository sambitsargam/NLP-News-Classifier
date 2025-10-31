"""
Download multiple news classification datasets
Including: BBC News, Reuters, Guardian, NYT, and other sources
"""

import os
import logging
import pandas as pd
import urllib.request
import json
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MultiSourceNewsDownloader:
    """Download news data from multiple sources"""
    
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(__file__), "..", "data")
        os.makedirs(self.data_path, exist_ok=True)
    
    def download_bbc_news_classifier(self):
        """Download BBC News Classification dataset (2225 samples, 5 categories)"""
        try:
            logger.info("📰 Downloading BBC News Classifier...")
            url = "https://raw.githubusercontent.com/susanli2016/PyCon-Canada-2019-NLP-Tutorial/master/bbc-text.csv"
            
            output_file = os.path.join(self.data_path, "bbc_news.csv")
            urllib.request.urlretrieve(url, output_file)
            
            df = pd.read_csv(output_file)
            
            if 'text' in df.columns and 'category' in df.columns:
                df_processed = df[['text', 'category']].dropna()
                logger.info(f"  ✓ BBC News: {len(df_processed)} samples")
                logger.info(f"  ✓ Categories: {df_processed['category'].unique().tolist()}")
                return output_file
        except Exception as e:
            logger.error(f"  ✗ Error: {e}")
        
        return None
    
    def download_ag_news(self):
        """Download AG News dataset (120,000 samples, 4 categories)"""
        try:
            logger.info("📰 Downloading AG News Dataset...")
            url = "https://raw.githubusercontent.com/mhjabreel/CharCnn_Keras/master/data/ag_news_csv/train.csv"
            
            output_file = os.path.join(self.data_path, "ag_news_train.csv")
            urllib.request.urlretrieve(url, output_file)
            
            df = pd.read_csv(output_file, header=None, names=['category_id', 'title', 'description'])
            
            category_map = {1: 'World', 2: 'Sports', 3: 'Business', 4: 'Science'}
            df['category'] = df['category_id'].map(category_map)
            df['text'] = df['title'] + ' ' + df['description']
            df_processed = df[['text', 'category']].dropna()
            
            output_processed = os.path.join(self.data_path, "ag_news_processed.csv")
            df_processed.to_csv(output_processed, index=False)
            
            logger.info(f"  ✓ AG News: {len(df_processed)} samples")
            logger.info(f"  ✓ Categories: {df_processed['category'].unique().tolist()}")
            return output_processed
        except Exception as e:
            logger.error(f"  ✗ Error: {e}")
        
        return None
    
    def download_20_newsgroups_converted(self):
        """Download 20 Newsgroups converted to news format"""
        try:
            logger.info("📰 Downloading 20 Newsgroups Dataset...")
            url = "https://raw.githubusercontent.com/kaushikjadhav01/News-Category-Classifier/master/data.csv"
            
            output_file = os.path.join(self.data_path, "20newsgroups.csv")
            urllib.request.urlretrieve(url, output_file)
            
            df = pd.read_csv(output_file)
            
            if 'NEWS' in df.columns and 'CATEGORY' in df.columns:
                df['text'] = df['NEWS']
                df['category'] = df['CATEGORY']
                df_processed = df[['text', 'category']].dropna()
                
                logger.info(f"  ✓ 20 Newsgroups: {len(df_processed)} samples")
                logger.info(f"  ✓ Categories: {df_processed['category'].unique().tolist()}")
                return output_file
        except Exception as e:
            logger.error(f"  ✗ Error: {e}")
        
        return None
    
    def download_bbc_news_archive(self):
        """Download BBC News Archive dataset"""
        try:
            logger.info("📰 Downloading BBC News Archive...")
            url = "https://raw.githubusercontent.com/rmunro/twitter_labor/master/data_annotation/bbc_articles_v2.csv"
            
            output_file = os.path.join(self.data_path, "bbc_archive.csv")
            urllib.request.urlretrieve(url, output_file)
            
            df = pd.read_csv(output_file)
            
            if 'text' in df.columns and 'label' in df.columns:
                df['category'] = df['label']
                df_processed = df[['text', 'category']].dropna()
                
                logger.info(f"  ✓ BBC Archive: {len(df_processed)} samples")
                logger.info(f"  ✓ Categories: {df_processed['category'].unique().tolist()}")
                return output_file
        except Exception as e:
            logger.error(f"  ✗ Error: {e}")
        
        return None
    
    def download_dbpedia_dataset(self):
        """Download DBpedia News Classification dataset (340,000 samples, 14 categories)"""
        try:
            logger.info("📰 Downloading DBpedia News Dataset...")
            url = "https://raw.githubusercontent.com/facebookresearch/fastText/master/data/dbpedia.train"
            
            output_file = os.path.join(self.data_path, "dbpedia_train.txt")
            urllib.request.urlretrieve(url, output_file)
            
            # Parse fastText format
            texts = []
            categories = []
            
            with open(output_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        parts = line.strip().split(' ', 1)
                        if len(parts) == 2:
                            category = parts[0].replace('__label__', '')
                            text = parts[1]
                            categories.append(category)
                            texts.append(text)
            
            df = pd.DataFrame({'text': texts, 'category': categories})
            
            output_processed = os.path.join(self.data_path, "dbpedia_processed.csv")
            df.to_csv(output_processed, index=False)
            
            logger.info(f"  ✓ DBpedia: {len(df)} samples")
            logger.info(f"  ✓ Categories: {df['category'].unique().tolist()}")
            return output_processed
        except Exception as e:
            logger.error(f"  ✗ Error: {e}")
        
        return None
    
    def download_sogou_news(self):
        """Download Sogou News Classification dataset"""
        try:
            logger.info("📰 Downloading Sogou News Dataset...")
            url = "https://raw.githubusercontent.com/zhangxiangxiao/Crepe/master/data/sogou_news/train.csv"
            
            output_file = os.path.join(self.data_path, "sogou_news.csv")
            urllib.request.urlretrieve(url, output_file)
            
            df = pd.read_csv(output_file)
            
            if len(df.columns) >= 2:
                df.columns = ['category', 'text'] + list(df.columns[2:])
                df_processed = df[['text', 'category']].dropna()
                
                logger.info(f"  ✓ Sogou News: {len(df_processed)} samples")
                logger.info(f"  ✓ Categories: {df_processed['category'].unique().tolist()}")
                return output_file
        except Exception as e:
            logger.error(f"  ✗ Error: {e}")
        
        return None
    
    def download_news_category_kaggle(self):
        """Download News Category Dataset from Kaggle"""
        try:
            logger.info("📰 Downloading News Category Dataset...")
            url = "https://raw.githubusercontent.com/rmunro/twitter_labor/master/data_annotation/news_category_dataset.csv"
            
            output_file = os.path.join(self.data_path, "news_category_dataset.csv")
            urllib.request.urlretrieve(url, output_file)
            
            df = pd.read_csv(output_file)
            
            if 'headline' in df.columns and 'category' in df.columns:
                df['text'] = df['headline']
                df_processed = df[['text', 'category']].dropna()
                
                logger.info(f"  ✓ News Category: {len(df_processed)} samples")
                logger.info(f"  ✓ Categories: {df_processed['category'].unique().tolist()}")
                return output_file
        except Exception as e:
            logger.error(f"  ✗ Error: {e}")
        
        return None
    
    def combine_all_datasets(self, datasets):
        """Combine all downloaded datasets"""
        try:
            all_dfs = []
            
            for dataset_path in datasets:
                if dataset_path and os.path.exists(dataset_path):
                    try:
                        df = pd.read_csv(dataset_path)
                        all_dfs.append(df)
                        logger.info(f"✓ Loaded {len(df)} from {Path(dataset_path).name}")
                    except Exception as e:
                        logger.warning(f"✗ Failed to load {Path(dataset_path).name}: {e}")
            
            if not all_dfs:
                logger.error("No datasets loaded successfully")
                return None
            
            # Combine
            combined_df = pd.concat(all_dfs, ignore_index=True)
            logger.info(f"\n📊 Combined dataset before cleaning: {len(combined_df)} samples")
            
            # Clean
            combined_df = combined_df.drop_duplicates(subset=['text'])
            combined_df = combined_df.dropna()
            
            # Filter text length
            combined_df['text_length'] = combined_df['text'].str.len()
            combined_df = combined_df[combined_df['text_length'] > 50]
            combined_df = combined_df[combined_df['text_length'] < 20000]
            combined_df = combined_df.drop('text_length', axis=1)
            
            # Normalize categories
            combined_df = self.normalize_categories(combined_df)
            
            # Remove categories with < 100 samples
            category_counts = combined_df['category'].value_counts()
            valid_categories = category_counts[category_counts >= 100].index
            combined_df = combined_df[combined_df['category'].isin(valid_categories)]
            
            logger.info(f"\n✅ Final dataset: {len(combined_df)} samples, {combined_df['category'].nunique()} categories")
            logger.info(f"Categories: {sorted(combined_df['category'].unique().tolist())}\n")
            logger.info("Category distribution:")
            print(combined_df['category'].value_counts())
            
            # Save
            output_file = os.path.join(self.data_path, "news_data_combined.csv")
            combined_df.to_csv(output_file, index=False)
            logger.info(f"\n✓ Saved combined dataset to {output_file}")
            
            return output_file
        
        except Exception as e:
            logger.error(f"Error combining datasets: {e}")
            return None
    
    def normalize_categories(self, df):
        """Normalize category names"""
        
        category_mapping = {
            'world': 'World',
            'sports': 'Sports',
            'sport': 'Sports',
            'business': 'Business',
            'science': 'Science',
            'technology': 'Technology',
            'tech': 'Technology',
            'entertainment': 'Entertainment',
            'politics': 'Politics',
            'political': 'Politics',
            'health': 'Health',
            'education': 'Education',
            'lifestyle': 'Lifestyle',
            'legal': 'Legal',
            'finance': 'Finance',
        }
        
        df['category'] = df['category'].str.lower().map(
            lambda x: category_mapping.get(x, x.title() if pd.notna(x) else 'Other')
        )
        
        return df


def main():
    """Main function to download all datasets"""
    
    downloader = MultiSourceNewsDownloader()
    
    logger.info("=" * 70)
    logger.info("🚀 DOWNLOADING MULTIPLE NEWS CLASSIFICATION DATASETS")
    logger.info("=" * 70)
    
    datasets = []
    
    # Download from all sources
    logger.info("\n[1/6] BBC News Classifier...")
    bbc = downloader.download_bbc_news_classifier()
    if bbc:
        datasets.append(bbc)
    
    logger.info("\n[2/6] AG News Dataset...")
    ag = downloader.download_ag_news()
    if ag:
        datasets.append(ag)
    
    logger.info("\n[3/6] 20 Newsgroups...")
    news20 = downloader.download_20_newsgroups_converted()
    if news20:
        datasets.append(news20)
    
    logger.info("\n[4/6] DBpedia News...")
    dbpedia = downloader.download_dbpedia_dataset()
    if dbpedia:
        datasets.append(dbpedia)
    
    logger.info("\n[5/6] Sogou News...")
    sogou = downloader.download_sogou_news()
    if sogou:
        datasets.append(sogou)
    
    logger.info("\n[6/6] News Category Dataset...")
    news_cat = downloader.download_news_category_kaggle()
    if news_cat:
        datasets.append(news_cat)
    
    # Combine all
    logger.info("\n" + "=" * 70)
    logger.info("🔗 COMBINING ALL DATASETS...")
    logger.info("=" * 70)
    
    combined = downloader.combine_all_datasets(datasets)
    
    if combined:
        logger.info("\n" + "=" * 70)
        logger.info("✅ DOWNLOAD AND COMBINATION COMPLETE!")
        logger.info("=" * 70)
        logger.info("\n📝 Next steps:")
        logger.info("   1. Run: python3.11 augment_data.py (to add missing categories)")
        logger.info("   2. Run: python3.11 train.py (to train the model)")
    else:
        logger.warning("❌ Failed to combine datasets")


if __name__ == "__main__":
    main()
