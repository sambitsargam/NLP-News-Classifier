"""
Generate synthetic news data for underrepresented categories
"""

import os
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


SYNTHETIC_NEWS = {
    'Politics': [
        "Government announces new policy framework for economic growth",
        "Parliament debates controversial legislation on environmental protection",
        "Political leaders call for diplomatic solutions to international tensions",
        "Policy makers discuss tax reform and budget allocation",
        "Government announces investment in infrastructure development",
        "Opposition party proposes alternative approach to healthcare",
        "Federal agency issues guidance on compliance standards",
        "Political campaign kicks off with major rally",
        "State governor signs new legislation on education reform",
        "Congress approves funding for scientific research initiatives",
        "Government commissions report on national security concerns",
        "Senate votes on judicial appointment to federal court",
        "President announces executive order on environmental protection",
        "Political activists organize demonstration for civil rights",
        "Government agencies coordinate disaster response efforts",
    ] * 1000,
    
    'Health': [
        "New clinical trial shows promising results for disease treatment",
        "Medical researchers develop innovative surgical procedure",
        "Public health officials launch vaccination campaign",
        "Hospital opens advanced research and treatment facility",
        "Scientists identify genetic factors in disease development",
        "Health organization releases new wellness guidelines",
        "Pharmaceutical company announces drug safety study results",
        "Medical team performs breakthrough surgical intervention",
        "Health authorities investigate disease outbreak",
        "Researchers publish findings on preventive medicine",
        "Hospital implements electronic health record system",
        "Medical training program receives accreditation",
        "Health professionals attend international conference",
        "Government allocates funds for health infrastructure",
        "Doctors announce new treatment protocol",
    ] * 1000,
    
    'Science': [
        "Scientists make breakthrough discovery in quantum mechanics",
        "Space agency launches new satellite mission",
        "Research team studies effects of climate change",
        "University announces new physics research center",
        "Scientists discover new species in rainforest expedition",
        "Laboratory develops advanced molecular testing method",
        "Research confirms theory about black holes",
        "Scientists study impact of pollution on ecosystems",
        "University receives grant for renewable energy research",
        "Research team publishes study on artificial intelligence",
        "Scientists develop new material for advanced applications",
        "Astronomers detect signals from distant galaxy",
        "Research institute conducts environmental survey",
        "Scientists present findings at international conference",
        "Laboratory discovers properties of rare element",
    ] * 1000,
    
    'World': [
        "International summit focuses on climate change solutions",
        "Countries sign trade agreement to boost economies",
        "United Nations addresses humanitarian crisis",
        "Global leaders discuss military cooperation",
        "World health organization coordinates pandemic response",
        "International court rules on territorial dispute",
        "Countries establish new alliance for security",
        "Global organization launches development initiative",
        "World leaders meet to discuss terrorism prevention",
        "International treaty signed by participating nations",
        "Global conference addresses education challenges",
        "International organization awards humanitarian prize",
        "Countries collaborate on scientific research project",
        "World summit discusses energy security issues",
        "International delegation visits neighboring country",
    ] * 800,
    
    'Lifestyle': [
        "Fashion designer unveils new collection at fashion week",
        "Travel guide highlights best destinations for vacation",
        "Home improvement expert shares renovation tips",
        "Celebrity chef opens new restaurant downtown",
        "Fitness instructor releases new workout program",
        "Wellness expert discusses mental health benefits",
        "Interior designer transforms home office space",
        "Travel blog features hidden gems in region",
        "Fashion brand launches sustainable clothing line",
        "Lifestyle coach provides tips for work-life balance",
        "Cooking show features traditional cuisine preparation",
        "Travel vlogger explores exotic destination",
        "Beauty brand announces skincare product launch",
        "Home automation expert discusses smart living",
        "Lifestyle influencer shares wellness routine",
    ] * 800,
    
    'Education': [
        "University announces new scholarship program for students",
        "Education technology platform improves learning outcomes",
        "School district implements innovative curriculum",
        "Teacher recognized for excellence in education",
        "Online learning platform expands course offerings",
        "Education ministry introduces new testing standards",
        "Student awarded prestigious academic fellowship",
        "Educational institution accredits advanced program",
        "University partners with industry for research",
        "School opens modern science and technology center",
        "Education conference discusses teaching innovations",
        "Scholarship foundation supports disadvantaged students",
        "University ranks among top institutions globally",
        "Educational nonprofit provides learning resources",
        "Teacher training program receives recognition",
    ] * 800,
    
    'Legal': [
        "Supreme court issues ruling on constitutional matter",
        "Law enforcement announces new policing strategy",
        "Legal experts debate recent court decision",
        "Attorney general files lawsuit against company",
        "Court sentences defendant in high-profile case",
        "Law firm wins landmark case for client",
        "Judge issues order regarding civil rights",
        "Government agency enforces compliance regulations",
        "Legal system reforms implemented by legislature",
        "Court case draws significant public attention",
        "Law enforcement agency conducts investigation",
        "Legal aid organization helps low-income clients",
        "Bar association disciplines attorney for misconduct",
        "Court establishes precedent for future cases",
        "Federal judge rules on constitutional rights",
    ] * 700,
    
    'Finance': [
        "Banking sector reports strong quarterly earnings",
        "Investment firm launches new mutual fund offering",
        "Financial advisors recommend diversified portfolio",
        "Stock market reaches historic high levels",
        "Federal reserve announces interest rate decision",
        "Cryptocurrency market experiences volatility",
        "Financial technology startup receives investment",
        "Economists predict sustained economic growth",
        "Insurance company expands product offerings",
        "Investment banking firm completes major deal",
        "Financial institution opens new branch",
        "Loan programs help small businesses expand",
        "Stock exchange adds new listed companies",
        "Financial markets respond to policy announcement",
        "Wealth management firm acquires competitor",
    ] * 700,
}


def generate_synthetic_data():
    """Generate synthetic data to balance all categories"""
    
    data_path = os.path.join(os.path.dirname(__file__), "..", "data")
    combined_file = os.path.join(data_path, "news_data_combined.csv")
    
    # Load existing data
    df = pd.read_csv(combined_file)
    
    # Create synthetic dataframe
    synthetic_texts = []
    synthetic_categories = []
    
    for category, texts in SYNTHETIC_NEWS.items():
        synthetic_texts.extend(texts)
        synthetic_categories.extend([category] * len(texts))
    
    synthetic_df = pd.DataFrame({
        'text': synthetic_texts,
        'category': synthetic_categories
    })
    
    # Combine
    combined = pd.concat([df, synthetic_df], ignore_index=True)
    
    # Remove duplicates
    combined = combined.drop_duplicates(subset=['text'])
    
    # Save
    output_file = os.path.join(data_path, "news_data_combined.csv")
    combined.to_csv(output_file, index=False)
    
    logger.info(f"{'='*60}")
    logger.info(f"Final dataset: {len(combined)} samples")
    logger.info(f"Total categories: {combined['category'].nunique()}")
    logger.info(f"Categories: {sorted(combined['category'].unique().tolist())}")
    logger.info(f"{'='*60}")
    logger.info(f"Category distribution:")
    print(combined['category'].value_counts().sort_index())
    logger.info(f"✓ Saved to {output_file}")


if __name__ == "__main__":
    generate_synthetic_data()
