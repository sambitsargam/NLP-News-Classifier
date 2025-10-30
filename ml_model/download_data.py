"""
Data Download Script
Downloads real news data from the internet for training and testing
"""

import os
import csv
import json
import logging
from typing import List, Tuple
import urllib.request
import urllib.error

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NewsDataDownloader:
    """Download news data from various sources"""
    
    def __init__(self, output_dir: str = "data"):
        """Initialize downloader"""
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def download_from_newsapi(self, api_key: str = None) -> List[Tuple[str, str]]:
        """
        Download from NewsAPI (requires free API key from https://newsapi.org)
        """
        if not api_key:
            logger.info("NewsAPI key not provided. Skipping NewsAPI data.")
            return []
        
        try:
            articles = []
            categories = {
                'business': 'Business',
                'entertainment': 'Entertainment',
                'health': 'Health',
                'science': 'Science',
                'sports': 'Sports',
                'technology': 'Technology',
                'politics': 'Politics'
            }
            
            for category, label in categories.items():
                url = f"https://newsapi.org/v2/top-headlines?category={category}&sortBy=popularity&apiKey={api_key}"
                try:
                    with urllib.request.urlopen(url) as response:
                        data = json.loads(response.read().decode())
                        if data.get('articles'):
                            for article in data['articles'][:5]:
                                text = f"{article.get('title', '')} {article.get('description', '')}"
                                if text.strip():
                                    articles.append((text, label))
                    logger.info(f"Downloaded {len([a for a in articles if a[1] == label])} articles for {category}")
                except Exception as e:
                    logger.warning(f"Error downloading {category}: {e}")
            
            return articles
        except Exception as e:
            logger.error(f"Error with NewsAPI: {e}")
            return []
    
    def get_sample_dataset(self) -> List[Tuple[str, str]]:
        """
        Return a comprehensive sample dataset of news articles
        This provides realistic news content for training
        """
        dataset = [
            # Sports
            ("Liverpool defeats Manchester United 3-1 in the Premier League match. The victory secures their position at the top of the table.", "Sports"),
            ("Tennis champion Novak Djokovic wins the Australian Open after a thrilling five-set match against Matteo Berrettini.", "Sports"),
            ("NBA Finals: Golden State Warriors claim their fourth championship in five years with a dominant performance.", "Sports"),
            ("Cricket: India's cricket team wins the test series against Australia with an impressive victory in the final match.", "Sports"),
            ("Formula 1: Lewis Hamilton sets a new track record at Monaco Grand Prix qualifying session.", "Sports"),
            ("Football: Argentina wins the Copa America final against Brazil in a penalty shootout.", "Sports"),
            ("NFL: Kansas City Chiefs become Super Bowl champions after defeating San Francisco 49ers.", "Sports"),
            
            # Politics
            ("New legislation passes Congress with bipartisan support for infrastructure development worth $1 trillion.", "Politics"),
            ("Presidential election campaign heats up as candidates debate key policy issues in televised debate.", "Politics"),
            ("Parliament approves new climate change bill aimed at reducing carbon emissions by 50% by 2030.", "Politics"),
            ("Prime Minister announces new economic policy focusing on job creation and small business support.", "Politics"),
            ("Senate confirms new Supreme Court Justice after contentious hearings and votes.", "Politics"),
            ("Trade negotiations between US and EU conclude with new agreement on tariffs.", "Politics"),
            ("Government announces new immigration reform policy amid ongoing political debate.", "Politics"),
            
            # Technology
            ("Apple releases new iPhone 15 with advanced AI features and improved camera system.", "Technology"),
            ("OpenAI unveils GPT-5, a breakthrough in artificial intelligence with improved reasoning capabilities.", "Technology"),
            ("Tesla announces new battery technology that doubles electric vehicle range.", "Technology"),
            ("Meta launches new virtual reality headset designed for metaverse applications.", "Technology"),
            ("Microsoft releases Windows 12 with integrated AI assistant and improved performance.", "Technology"),
            ("Google announces quantum computing breakthrough solving previously unsolvable problems.", "Technology"),
            ("Semiconductor shortage eases as chip manufacturers increase production capacity.", "Technology"),
            
            # Entertainment
            ("Oscars 2024: Avatar 3 wins Best Picture in historic ceremony honoring cinema.", "Entertainment"),
            ("Taylor Swift announces world tour with record-breaking ticket sales in one day.", "Entertainment"),
            ("Netflix releases highly anticipated series that breaks viewing records on opening day.", "Entertainment"),
            ("New James Bond film exceeds box office expectations with $700 million worldwide earnings.", "Entertainment"),
            ("Music festival lineup announced featuring top international artists and performers.", "Entertainment"),
            ("Grammy Awards: Beyonce wins multiple awards including Album of the Year.", "Entertainment"),
            ("Disney releases new animated film that becomes highest-grossing movie of the quarter.", "Entertainment"),
            
            # Business
            ("Stock market reaches all-time high as major indices post strong quarterly gains.", "Business"),
            ("Tech startup raises $500 million in Series C funding at $2 billion valuation.", "Business"),
            ("Microsoft and Google announce strategic partnership for cloud computing services.", "Business"),
            ("Corporate earnings beat analyst expectations with strong revenue growth reported.", "Business"),
            ("Oil prices surge following OPEC announcement of production cuts.", "Business"),
            ("Cryptocurrency market experiences volatility as Bitcoin price fluctuates dramatically.", "Business"),
            ("Major merger deal announced between two Fortune 500 companies for $50 billion.", "Business"),
            
            # Health
            ("FDA approves breakthrough cancer drug showing 90% efficacy in clinical trials.", "Health"),
            ("New study reveals exercise and meditation reduce anxiety and depression significantly.", "Health"),
            ("Health officials warn of new virus variant spreading across multiple countries.", "Health"),
            ("Pharmaceutical company announces vaccine for Alzheimer's disease with promising results.", "Health"),
            ("WHO declares global health emergency as disease outbreak spreads internationally.", "Health"),
            ("Mental health awareness campaign launched to address rising depression rates.", "Health"),
            ("Hospital implements new AI diagnostic system improving accuracy of disease detection.", "Health"),
            
            # Science
            ("Scientists discover new species of deep-sea creature in Arctic waters.", "Science"),
            ("SpaceX successfully launches satellite to expand global internet coverage.", "Science"),
            ("Researchers discover ancient fossils proving new evolutionary pathway.", "Science"),
            ("Climate scientists publish report showing acceleration of global warming trends.", "Science"),
            ("Physicists achieve breakthrough in quantum computing research at CERN.", "Science"),
            ("Astronomers detect radio signals from distant galaxy suggesting possible life.", "Science"),
            ("Biologists unlock DNA secrets of longevity in centenarians through new research.", "Science"),
        ]
        
        return dataset
    
    def save_as_csv(self, articles: List[Tuple[str, str]], filename: str = "news_data.csv"):
        """Save articles as CSV file"""
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['text', 'category'])
                writer.writerows(articles)
            
            logger.info(f"Saved {len(articles)} articles to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error saving CSV: {e}")
            return None
    
    def save_as_json(self, articles: List[Tuple[str, str]], filename: str = "news_data.json"):
        """Save articles as JSON file"""
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            data = [
                {"text": text, "category": category}
                for text, category in articles
            ]
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved {len(articles)} articles to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error saving JSON: {e}")
            return None
    
    def download_all(self, api_key: str = None):
        """Download from all sources and save"""
        logger.info("Starting data download...")
        
        # Get sample dataset
        articles = self.get_sample_dataset()
        logger.info(f"Loaded {len(articles)} sample articles")
        
        # Try to download from NewsAPI if key provided
        if api_key:
            try:
                newsapi_articles = self.download_from_newsapi(api_key)
                articles.extend(newsapi_articles)
                logger.info(f"Total articles after NewsAPI: {len(articles)}")
            except Exception as e:
                logger.warning(f"NewsAPI download failed: {e}")
        
        # Save in multiple formats
        self.save_as_csv(articles, "news_data.csv")
        self.save_as_json(articles, "news_data.json")
        
        # Create summary
        self._create_summary(articles)
        
        logger.info(f"✓ Download complete! Total articles: {len(articles)}")
        return articles
    
    def _create_summary(self, articles: List[Tuple[str, str]]):
        """Create summary of downloaded data"""
        summary_path = os.path.join(self.output_dir, "data_summary.txt")
        
        categories = {}
        for text, category in articles:
            categories[category] = categories.get(category, 0) + 1
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write("NEWS DATASET SUMMARY\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Total Articles: {len(articles)}\n")
            f.write(f"Total Categories: {len(categories)}\n\n")
            f.write("Articles per Category:\n")
            f.write("-" * 50 + "\n")
            for category in sorted(categories.keys()):
                count = categories[category]
                f.write(f"  {category}: {count} articles\n")
        
        logger.info(f"Summary saved to {summary_path}")


def main():
    """Main function"""
    import sys
    
    # Optional: Pass NewsAPI key as argument
    api_key = sys.argv[1] if len(sys.argv) > 1 else None
    
    downloader = NewsDataDownloader(output_dir="../data")
    downloader.download_all(api_key)
    
    print("\n✅ Data download complete!")
    print("Files created:")
    print("  - data/news_data.csv (CSV format)")
    print("  - data/news_data.json (JSON format)")
    print("  - data/data_summary.txt (Statistics)")


if __name__ == "__main__":
    main()
