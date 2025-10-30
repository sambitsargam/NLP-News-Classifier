"""
Model Training Script
Train and save the news classifier model using downloaded data
"""

import os
import logging
import csv
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NewsClassifierTrainer:
    """Trainer for news classification model"""
    
    CATEGORIES = [
        "Sports",
        "Politics",
        "Technology",
        "Entertainment",
        "Business",
        "Health",
        "Science"
    ]
    
    def __init__(self, data_path: str = None):
        """Initialize the trainer"""
        self.data_path = data_path or os.path.join(
            os.path.dirname(__file__),
            "..",
            "data"
        )
        self.model_path = os.path.join(os.path.dirname(__file__), "models")
        os.makedirs(self.model_path, exist_ok=True)
    
    def load_data(self, csv_file: str = None) -> tuple:
        """
        Load training data from CSV or use sample data
        Expected CSV format: text, category
        
        Args:
            csv_file: Path to CSV file with columns 'text' and 'category'
            
        Returns:
            Tuple of (texts, labels, unique_categories)
        """
        # Try to load from downloaded data first
        if csv_file is None:
            csv_file = os.path.join(self.data_path, "news_data.csv")
        
        if os.path.exists(csv_file):
            try:
                texts = []
                labels = []
                unique_categories = set()
                
                with open(csv_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        texts.append(row['text'])
                        labels.append(row['category'])
                        unique_categories.add(row['category'])
                
                logger.info(f"Loaded {len(texts)} samples from {csv_file}")
                return texts, labels, sorted(list(unique_categories))
            except Exception as e:
                logger.warning(f"Error loading CSV: {e}. Using sample data instead.")
        
        # Fallback to sample data
        logger.info("Using built-in sample data for training...")
        return self._get_sample_data()
    
    def _get_sample_data(self) -> tuple:
        """
        Create comprehensive sample training data for demonstration
        """
        sample_texts = {
            "Sports": [
                "The championship game was thrilling. The team scored in the final minutes.",
                "Athletes are training hard for the upcoming marathon competition.",
                "The football season starts next month with new draft picks.",
                "Tennis players compete for the grand slam title.",
                "The soccer match ended with a spectacular goal.",
                "Basketball team wins playoff series with overtime victory.",
                "Cricket match becomes historic with record-breaking innings.",
                "Olympic athletes prepare for international competition."
            ],
            "Politics": [
                "New legislation was passed by the parliament today.",
                "The political debate centers on healthcare policy.",
                "The presidential election is coming next year.",
                "Congress members discuss budget allocation.",
                "Political campaigns intensify in key states.",
                "Senate approves new trade agreement with allies.",
                "Political leaders meet for international summit.",
                "Government announces new policy on taxation."
            ],
            "Technology": [
                "New AI breakthrough announced by tech company.",
                "Smartphone technology reaches new heights with faster processors.",
                "Cybersecurity threats increase as hacking attempts rise.",
                "Tech startups raise millions in funding rounds.",
                "Cloud computing infrastructure sees rapid growth.",
                "Artificial intelligence transforms business operations.",
                "Software company releases groundbreaking application.",
                "Tech giants compete for market dominance."
            ],
            "Entertainment": [
                "The movie premiere was attended by celebrities.",
                "Music festival features top artists and bands.",
                "New TV series launches on streaming platform.",
                "Celebrity gossip and news from Hollywood.",
                "Award ceremony celebrates entertainment industry.",
                "Actor wins prestigious award for outstanding performance.",
                "Concert tour announces additional dates due to demand.",
                "Film breaks box office records on opening weekend."
            ],
            "Business": [
                "Stock market reaches all-time high.",
                "Corporate earnings exceed analyst expectations.",
                "New business partnerships announced.",
                "Startup founders share growth strategies.",
                "Economic indicators show strong market performance.",
                "Company announces major acquisition deal.",
                "Investors show confidence in emerging markets.",
                "Business leaders discuss global economy trends."
            ],
            "Health": [
                "New medical research shows positive results.",
                "Healthcare system faces challenges.",
                "Fitness tips for maintaining good health.",
                "Medical breakthrough in disease treatment.",
                "Mental health awareness campaign launches.",
                "Doctors recommend preventive health measures.",
                "Hospital implements new treatment protocol.",
                "Healthcare workers receive recognition and awards."
            ],
            "Science": [
                "Scientists discover new species in rainforest.",
                "Space exploration mission successful.",
                "Climate change research reveals critical findings.",
                "Physics experiment yields surprising results.",
                "Biology research advances human understanding.",
                "Environmental scientists study pollution impact.",
                "Researchers make quantum physics breakthrough.",
                "Scientific community celebrates discovery milestone."
            ]
        }
        
        texts = []
        labels = []
        
        for category in self.CATEGORIES:
            if category in sample_texts:
                texts.extend(sample_texts[category])
                labels.extend([category] * len(sample_texts[category]))
        
        logger.info(f"Created sample dataset with {len(texts)} samples")
        
        return texts, labels, self.CATEGORIES
    
    def train(self, texts: list, labels: list) -> tuple:
        """
        Train the classifier model
        
        Args:
            texts: List of text samples
            labels: List of labels (category names)
            
        Returns:
            Tuple of (pipeline, metrics)
        """
        logger.info(f"Training on {len(texts)} samples")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            texts, labels, test_size=0.2, random_state=42, stratify=labels
        )
        
        logger.info(f"Training set: {len(X_train)}, Test set: {len(X_test)}")
        
        # Create pipeline
        pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=1000, stop_words='english')),
            ('classifier', MultinomialNB())
        ])
        
        # Train
        pipeline.fit(X_train, y_train)
        
        # Evaluate
        y_pred = pipeline.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        logger.info(f"Model trained with accuracy: {accuracy:.4f}")
        logger.info(f"\nClassification Report:\n{classification_report(y_test, y_pred)}")
        
        metrics = {
            "accuracy": accuracy,
            "train_size": len(X_train),
            "test_size": len(X_test)
        }
        
        return pipeline, metrics
    
    def save_model(self, pipeline, metrics):
        """Save model and metrics"""
        try:
            # Save pipeline (contains both vectorizer and classifier)
            joblib.dump(pipeline, os.path.join(self.model_path, "sklearn_model.joblib"))
            
            # Save metrics
            joblib.dump(metrics, os.path.join(self.model_path, "metrics.joblib"))
            
            logger.info(f"✓ Model saved to {self.model_path}")
        except Exception as e:
            logger.error(f"Error saving model: {e}")
            raise


def main():
    """Main training function"""
    trainer = NewsClassifierTrainer()
    
    # Load data (will try downloaded data first, then sample data)
    texts, labels, categories = trainer.load_data()
    
    logger.info(f"Categories: {categories}")
    logger.info(f"Total samples: {len(texts)}")
    
    # Train
    pipeline, metrics = trainer.train(texts, labels)
    
    # Save
    trainer.save_model(pipeline, metrics)
    
    logger.info("✓ Training completed successfully!")


if __name__ == "__main__":
    main()
