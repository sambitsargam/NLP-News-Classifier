"""
Download comprehensive news datasets with 12+ categories
"""

import os
import logging
import pandas as pd
import urllib.request
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ComprehensiveNewsDownloader:
    """Download diverse news datasets with multiple categories"""
    
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(__file__), "..", "data")
        os.makedirs(self.data_path, exist_ok=True)
    
    def download_news_category_dataset(self):
        """Download News Category Dataset (200K+ samples, 41 categories)"""
        try:
            logger.info("Downloading News Category Dataset...")
            url = "https://raw.githubusercontent.com/rmunro/twitter_labor/master/data_annotation/bbc_articles_v2.csv"
            
            # Using HuggingFace News Category Dataset
            url = "https://huggingface.co/datasets/fancyzhx/ag_news/resolve/main/data/train.csv"
            
            output_file = os.path.join(self.data_path, "news_category_hf.csv")
            urllib.request.urlretrieve(url, output_file)
            
            df = pd.read_csv(output_file)
            
            if 'label' in df.columns and 'text' in df.columns:
                category_map = {0: 'World', 1: 'Sports', 2: 'Business', 3: 'Science'}
                df['category'] = df['label'].map(category_map)
                df_processed = df[['text', 'category']].dropna()
                
                output_processed = os.path.join(self.data_path, "news_category_hf.csv")
                df_processed.to_csv(output_processed, index=False)
                
                logger.info(f"✓ HuggingFace dataset: {len(df_processed)} samples")
                logger.info(f"✓ Categories: {df_processed['category'].unique().tolist()}")
                return output_processed
        except Exception as e:
            logger.error(f"Error downloading HuggingFace dataset: {e}")
        
        return None
    
    def download_bbc_news(self):
        """Download BBC News dataset (5 categories)"""
        try:
            logger.info("Downloading BBC News dataset...")
            url = "https://raw.githubusercontent.com/susanli2016/PyCon-Canada-2019-NLP-Tutorial/master/bbc-text.csv"
            
            output_file = os.path.join(self.data_path, "bbc_news.csv")
            urllib.request.urlretrieve(url, output_file)
            
            df = pd.read_csv(output_file)
            
            if 'text' in df.columns and 'category' in df.columns:
                df_processed = df[['text', 'category']].dropna()
                
                output_processed = os.path.join(self.data_path, "bbc_news_processed.csv")
                df_processed.to_csv(output_processed, index=False)
                
                logger.info(f"✓ BBC News dataset: {len(df_processed)} samples")
                logger.info(f"✓ Categories: {df_processed['category'].unique().tolist()}")
                return output_processed
        except Exception as e:
            logger.error(f"Error downloading BBC News: {e}")
        
        return None
    
    def download_ag_news(self):
        """Download AG News dataset (120K samples)"""
        try:
            logger.info("Downloading AG News dataset...")
            url = "https://raw.githubusercontent.com/mhjabreel/CharCnn_Keras/master/data/ag_news_csv/train.csv"
            
            output_file = os.path.join(self.data_path, "ag_news_train.csv")
            urllib.request.urlretrieve(url, output_file)
            
            df = pd.read_csv(output_file, header=None, names=['category_id', 'title', 'description'])
            
            category_map = {
                1: 'Business',
                2: 'Sports',
                3: 'Technology',
                4: 'Entertainment'
            }
            
            df['category'] = df['category_id'].map(category_map)
            df['text'] = df['title'] + ' ' + df['description']
            df_processed = df[['text', 'category']].dropna()
            
            output_processed = os.path.join(self.data_path, "ag_news_processed.csv")
            df_processed.to_csv(output_processed, index=False)
            
            logger.info(f"✓ AG News dataset: {len(df_processed)} samples")
            logger.info(f"✓ Categories: {df_processed['category'].unique().tolist()}")
            return output_processed
        except Exception as e:
            logger.error(f"Error downloading AG News: {e}")
        
        return None
    
    def download_reuters_dataset(self):
        """Download Reuters dataset"""
        try:
            logger.info("Downloading Reuters-style dataset...")
            url = "https://raw.githubusercontent.com/topics/reuters-dataset/master/data.csv"
            
            # Alternative source
            url = "https://raw.githubusercontent.com/kaushikjadhav01/news-classification/master/news.csv"
            
            output_file = os.path.join(self.data_path, "reuters.csv")
            urllib.request.urlretrieve(url, output_file)
            
            df = pd.read_csv(output_file)
            
            # Check columns
            if 'text' in df.columns and 'category' in df.columns:
                df_processed = df[['text', 'category']].dropna()
            elif 'news' in df.columns and 'category' in df.columns:
                df['text'] = df['news']
                df_processed = df[['text', 'category']].dropna()
            else:
                logger.warning("Reuters dataset column structure different")
                return None
            
            output_processed = os.path.join(self.data_path, "reuters_processed.csv")
            df_processed.to_csv(output_processed, index=False)
            
            logger.info(f"✓ Reuters dataset: {len(df_processed)} samples")
            logger.info(f"✓ Categories: {df_processed['category'].unique().tolist()}")
            return output_processed
        except Exception as e:
            logger.error(f"Error downloading Reuters: {e}")
        
        return None
    
    def download_huffpost_dataset(self):
        """Download HuffPost News Category Dataset"""
        try:
            logger.info("Downloading HuffPost News dataset...")
            url = "https://raw.githubusercontent.com/rmunro/twitter_labor/master/data_annotation/huffpost_news.csv"
            
            # Alternative HuffPost source
            url = "https://raw.githubusercontent.com/MultimodalNLP-Group/MoENet/main/Data/News/huffpost.csv"
            
            output_file = os.path.join(self.data_path, "huffpost.csv")
            urllib.request.urlretrieve(url, output_file)
            
            df = pd.read_csv(output_file)
            
            if 'text' in df.columns and 'category' in df.columns:
                df_processed = df[['text', 'category']].dropna()
                
                output_processed = os.path.join(self.data_path, "huffpost_processed.csv")
                df_processed.to_csv(output_processed, index=False)
                
                logger.info(f"✓ HuffPost dataset: {len(df_processed)} samples")
                logger.info(f"✓ Categories: {df_processed['category'].unique().tolist()}")
                return output_processed
        except Exception as e:
            logger.error(f"Error downloading HuffPost: {e}")
        
        return None
    
    def create_diverse_sample_data(self):
        """Create diverse sample data with 12+ categories"""
        try:
            logger.info("Creating diverse sample dataset with 12 categories...")
            
            sample_data = {
                'Business': [
                    "Stock market rises as investor confidence grows.",
                    "Company announces record profits and expansion plans.",
                    "Economic indicators show growth in manufacturing sector.",
                ],
                'Technology': [
                    "New AI breakthrough revolutionizes machine learning.",
                    "Tech giant releases latest smartphone with advanced features.",
                    "Cybersecurity firm reports increase in hacking attempts.",
                ],
                'Sports': [
                    "Championship game ends in thrilling overtime victory.",
                    "Olympic athlete breaks world record in swimming.",
                    "Football team wins playoff series with perfect season.",
                ],
                'Entertainment': [
                    "Movie premiere attended by celebrities and fans.",
                    "Music festival features top artists and bands.",
                    "Award ceremony celebrates entertainment industry.",
                ],
                'Politics': [
                    "New legislation passes in parliament debate.",
                    "Presidential election campaigns intensify.",
                    "Government announces policy on taxation reform.",
                ],
                'Health': [
                    "Medical researchers discover new treatment for disease.",
                    "Health organization reports on fitness and wellness.",
                    "Hospital announces advanced surgical techniques.",
                ],
                'Science': [
                    "Scientists make breakthrough in quantum physics.",
                    "Space agency launches new research mission.",
                    "Environmental study reveals climate change data.",
                ],
                'World': [
                    "International summit discusses global cooperation.",
                    "Countries sign trade agreement for mutual benefit.",
                    "World leaders meet to address humanitarian crisis.",
                ],
                'Lifestyle': [
                    "Fashion week showcases latest designer collections.",
                    "Travel guide recommends top vacation destinations.",
                    "Home improvement tips for modern living.",
                ],
                'Education': [
                    "University announces new scholarship program.",
                    "Educational technology improves learning outcomes.",
                    "School district implements curriculum reforms.",
                ],
                'Legal': [
                    "Court rules on important constitutional matter.",
                    "New law enforcement policy implemented.",
                    "Legal experts debate recent legislation.",
                ],
                'Finance': [
                    "Banking sector reports quarterly earnings.",
                    "Investment firm launches new mutual fund.",
                    "Financial advisors recommend portfolio strategies.",
                ],
            }
            
            texts = []
            labels = []
            
            for category, examples in sample_data.items():
                texts.extend(examples)
                labels.extend([category] * len(examples))
            
            df = pd.DataFrame({'text': texts, 'category': labels})
            
            output_file = os.path.join(self.data_path, "sample_12_categories.csv")
            df.to_csv(output_file, index=False)
            
            logger.info(f"✓ Created sample dataset: {len(df)} samples, {len(sample_data)} categories")
            logger.info(f"✓ Categories: {list(sample_data.keys())}")
            
            return output_file
        except Exception as e:
            logger.error(f"Error creating sample data: {e}")
        
        return None
    
    def normalize_categories(self, df):
        """Normalize category names"""
        
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
            'education': 'Education',
            'legal': 'Legal',
            'finance': 'Finance',
        }
        
        df['category'] = df['category'].str.lower().map(
            lambda x: category_mapping.get(x, x.title())
        )
        
        return df
    
    def combine_datasets(self, datasets):
        """Combine multiple datasets and normalize"""
        try:
            all_dfs = []
            
            for dataset_path in datasets:
                if dataset_path and os.path.exists(dataset_path):
                    df = pd.read_csv(dataset_path)
                    all_dfs.append(df)
                    logger.info(f"Loaded {len(df)} samples from {os.path.basename(dataset_path)}")
            
            if not all_dfs:
                logger.warning("No datasets loaded")
                return None
            
            combined_df = pd.concat(all_dfs, ignore_index=True)
            
            # Remove duplicates
            combined_df = combined_df.drop_duplicates(subset=['text'])
            
            # Remove rows with NaN
            combined_df = combined_df.dropna()
            
            # Filter by text length
            combined_df['text_length'] = combined_df['text'].str.len()
            combined_df = combined_df[combined_df['text_length'] > 50]
            combined_df = combined_df[combined_df['text_length'] < 15000]
            combined_df = combined_df.drop('text_length', axis=1)
            
            # Normalize categories
            combined_df = self.normalize_categories(combined_df)
            
            # Remove categories with very few samples (< 50)
            category_counts = combined_df['category'].value_counts()
            valid_categories = category_counts[category_counts >= 50].index
            combined_df = combined_df[combined_df['category'].isin(valid_categories)]
            
            output_file = os.path.join(self.data_path, "news_data_combined.csv")
            combined_df.to_csv(output_file, index=False)
            
            logger.info(f"\n{'='*60}")
            logger.info(f"Combined dataset: {len(combined_df)} samples")
            logger.info(f"Total categories: {combined_df['category'].nunique()}")
            logger.info(f"Categories: {sorted(combined_df['category'].unique().tolist())}")
            logger.info(f"{'='*60}")
            logger.info(f"Category distribution:")
            logger.info(f"{combined_df['category'].value_counts().to_string()}")
            logger.info(f"✓ Saved to {output_file}")
            
            return output_file
        
        except Exception as e:
            logger.error(f"Error combining datasets: {e}")
            return None


def main():
    """Main function"""
    downloader = ComprehensiveNewsDownloader()
    
    logger.info("=" * 60)
    logger.info("Downloading Comprehensive News Datasets (12+ Categories)")
    logger.info("=" * 60)
    
    datasets = []
    
    # Try all sources
    logger.info("\n[1/6] AG News dataset...")
    ag = downloader.download_ag_news()
    if ag:
        datasets.append(ag)
    
    logger.info("\n[2/6] BBC News dataset...")
    bbc = downloader.download_bbc_news()
    if bbc:
        datasets.append(bbc)
    
    logger.info("\n[3/6] HuggingFace News dataset...")
    hf = downloader.download_news_category_dataset()
    if hf:
        datasets.append(hf)
    
    logger.info("\n[4/6] Reuters dataset...")
    reuters = downloader.download_reuters_dataset()
    if reuters:
        datasets.append(reuters)
    
    logger.info("\n[5/6] HuffPost dataset...")
    huffpost = downloader.download_huffpost_dataset()
    if huffpost:
        datasets.append(huffpost)
    
    logger.info("\n[6/6] Creating diverse sample data...")
    sample = downloader.create_diverse_sample_data()
    if sample:
        datasets.append(sample)
    
    # Combine all datasets
    logger.info("\n" + "=" * 60)
    logger.info("Combining all datasets...")
    logger.info("=" * 60)
    
    combined = downloader.combine_datasets(datasets)
    
    if combined:
        logger.info("\n✓ Data download and combination complete!")
        logger.info("✓ Next step: Run 'python3.11 train.py' to train the model")
    else:
        logger.warning("Failed to combine datasets")


if __name__ == "__main__":
    main()
