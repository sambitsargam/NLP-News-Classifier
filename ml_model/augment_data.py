"""
Augment dataset with synthetic news articles to create 12 categories
"""

import os
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def augment_with_synthetic_data():
    """Add synthetic news data for missing categories"""
    
    data_path = os.path.join(os.path.dirname(__file__), "..", "data")
    combined_file = os.path.join(data_path, "news_data_combined.csv")
    
    # Load existing data
    df = pd.read_csv(combined_file)
    logger.info(f"Loaded combined dataset: {len(df)} samples")
    
    # Synthetic data for additional categories
    synthetic_data = {
        'Health': [
            "Health officials report new vaccine successfully tested.",
            "Medical breakthrough in cancer treatment research announced.",
            "Hospital implements new surgical techniques.",
            "Public health campaign launches awareness initiative.",
            "Pharmaceutical company develops new drug treatment.",
            "Health ministry issues new guidelines for wellness.",
            "Medical team completes successful transplant surgery.",
            "Research shows benefits of regular exercise.",
        ] * 3000,
        'Science': [
            "Scientists discover new particle in physics research.",
            "Space agency announces successful mission launch.",
            "Research team makes breakthrough in genetics.",
            "Climate scientists release new environmental data.",
            "University announces new research facility opening.",
            "Scientists publish findings on renewable energy.",
            "Research community celebrates scientific discovery.",
            "Laboratory develops new testing methodology.",
        ] * 3000,
        'World': [
            "International organization discusses global cooperation.",
            "World leaders meet for diplomatic summit.",
            "Countries announce new trade agreements.",
            "Global health organization addresses crisis.",
            "International court rules on important case.",
            "United Nations addresses humanitarian issues.",
            "Global conference discusses climate action.",
            "World powers negotiate peace agreement.",
        ] * 2000,
        'Lifestyle': [
            "Fashion industry announces latest trends.",
            "Travel guide features top destinations.",
            "Home improvement tips shared by experts.",
            "Cooking show features celebrity chef.",
            "Fitness trainer releases new workout plan.",
            "Beauty and wellness products reviewed.",
            "Interior design inspiration for modern homes.",
            "Travel blogger shares adventure stories.",
        ] * 2000,
        'Education': [
            "University announces scholarship program.",
            "Educational technology improves learning.",
            "School district implements new curriculum.",
            "Teacher receives award for excellence.",
            "Online learning platform gains popularity.",
            "Education ministry updates policies.",
            "Student achieves outstanding academic results.",
            "Education conference discusses innovations.",
        ] * 2000,
        'Legal': [
            "Court rules on constitutional matter.",
            "Law enforcement announces new policy.",
            "Legal experts debate legislation.",
            "Supreme court decision affects public.",
            "Attorney general issues guidance.",
            "Law enforcement increases patrols.",
            "Legal system reforms implemented.",
            "Court case draws public attention.",
        ] * 1500,
        'Finance': [
            "Banking sector reports earnings.",
            "Investment firm launches new fund.",
            "Financial advisors recommend strategies.",
            "Stock market shows strong performance.",
            "Federal reserve makes policy decision.",
            "Cryptocurrency market shows volatility.",
            "Financial technology startup raises capital.",
            "Economists predict economic growth.",
        ] * 1500,
    }
    
    # Create synthetic dataframe
    synthetic_texts = []
    synthetic_categories = []
    
    for category, texts in synthetic_data.items():
        synthetic_texts.extend(texts)
        synthetic_categories.extend([category] * len(texts))
    
    synthetic_df = pd.DataFrame({
        'text': synthetic_texts,
        'category': synthetic_categories
    })
    
    # Combine with existing data
    combined = pd.concat([df, synthetic_df], ignore_index=True)
    
    # Remove duplicates
    combined = combined.drop_duplicates(subset=['text'])
    
    # Save
    output_file = os.path.join(data_path, "news_data_combined.csv")
    combined.to_csv(output_file, index=False)
    
    logger.info(f"\n{'='*60}")
    logger.info(f"Augmented dataset: {len(combined)} samples")
    logger.info(f"Total categories: {combined['category'].nunique()}")
    logger.info(f"Categories: {sorted(combined['category'].unique().tolist())}")
    logger.info(f"{'='*60}")
    logger.info(f"Category distribution:")
    logger.info(f"{combined['category'].value_counts().to_string()}")
    logger.info(f"✓ Saved to {output_file}")
    
    return combined


if __name__ == "__main__":
    augment_with_synthetic_data()
