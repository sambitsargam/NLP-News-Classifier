# Machine Learning Models Documentation

## Overview

The News Category Classifier employs two distinct machine learning algorithms for news classification:

1. **Sklearn Model** - Fast, lightweight TF-IDF + Multinomial Naive Bayes
2. **Transformer Model** - Advanced BART-based zero-shot classification

---

## 1. Sklearn Model (TF-IDF + Multinomial Naive Bayes)

### Architecture

```
Input Text
    ↓
Text Preprocessing (cleaning, tokenization)
    ↓
TF-IDF Vectorization (1000 features)
    ↓
Multinomial Naive Bayes Classifier
    ↓
Probability Scores & Category Prediction
```

### Algorithm Details

#### A. TF-IDF Vectorization

**TF-IDF** (Term Frequency-Inverse Document Frequency) converts raw text into numerical vectors:

- **Term Frequency (TF)**: Measures how often a term appears in a document
  ```
  TF(t,d) = (Count of term t in document d) / (Total terms in document d)
  ```

- **Inverse Document Frequency (IDF)**: Measures the importance of a term across the corpus
  ```
  IDF(t) = log(Total documents / Documents containing term t)
  ```

- **TF-IDF Score**:
  ```
  TF-IDF(t,d) = TF(t,d) × IDF(t)
  ```

**Configuration:**
- Max features: 1000 (keeps the 1000 most important words)
- Stop words: English stop words removed (the, a, is, etc.)
- Lowercase: All text converted to lowercase
- N-grams: Unigrams (individual words)

**Advantages:**
- Fast computation
- Efficient memory usage
- Works well with sparse text data
- Interpretable feature importance

#### B. Multinomial Naive Bayes

A probabilistic classifier based on Bayes' theorem optimized for discrete feature counts (word frequencies):

**Mathematical Formulation:**

```
P(Category|Document) = P(Document|Category) × P(Category) / P(Document)

For text classification with conditional independence assumption:
P(Document|Category) = ∏ P(word_i|Category)^count(word_i)

Where:
- P(word_i|Category) = (count of word_i in category + 1) / (total words in category + vocabulary size)
- Laplace smoothing (add 1) prevents zero probabilities
```

**Decision Rule:**
```
Predicted Category = argmax_c P(Category_c|Document)
                   = argmax_c log(P(Category_c)) + Σ log(P(word_i|Category_c))
```

**Advantages:**
- Fast training and prediction
- Works well with high-dimensional sparse data
- Probabilistic predictions (confidence scores)
- Good baseline for text classification

**Disadvantages:**
- Assumes word independence (not always true)
- May underperform on complex linguistic patterns
- Limited context understanding

### Training Process

1. **Data Loading**: 120,577 news articles across 12 categories
2. **Preprocessing**: Text cleaning and tokenization
3. **Vectorization**: TF-IDF transformation
4. **Model Training**: Naive Bayes learns category probabilities
5. **Evaluation**: 85% accuracy on test set

### Performance Metrics

| Metric | Score |
|--------|-------|
| Overall Accuracy | 85% |
| Training Samples | 96,461 |
| Test Samples | 24,116 |
| Categories | 12 |
| Processing Speed | ~5-10ms per article |

### Category-Specific Performance

| Category | Precision | Recall | F1-Score |
|----------|-----------|--------|----------|
| Business | 0.85 | 0.86 | 0.85 |
| Entertainment | 0.81 | 0.80 | 0.81 |
| Sports | 0.90 | 0.94 | 0.92 |
| Technology | 0.82 | 0.79 | 0.81 |
| Politics | High | Varies | Moderate |
| Others | Varies | Varies | Varies |

---

## 2. Transformer Model (BART Zero-Shot Classification)

### Architecture

```
Input Text
    ↓
Tokenization & Encoding
    ↓
BART Transformer Encoder
    ↓
Attention Mechanisms
    ↓
Probability Distribution Across Categories
    ↓
Category Prediction & Confidence Scores
```

### Algorithm Details

#### A. BART (Denoising Autoencoder Transformer)

**Overview:**
BART (Bidirectional and Auto-Regressive Transformers) is a denoising autoencoder that combines:
- **Bidirectional Encoder** (like BERT)
- **Auto-Regressive Decoder** (like GPT)

**Key Components:**

1. **Tokenization**
   - Uses BPE (Byte Pair Encoding) tokenizer
   - Converts text to token IDs
   - Special tokens: `<s>` (start), `</s>` (end), `<unk>` (unknown)

2. **Embedding Layer**
   ```
   Token Embedding + Positional Embedding = Input Representation
   
   Where:
   - Token Embedding: Learned vector for each token
   - Positional Embedding: Encodes position information
   ```

3. **Transformer Encoder Layers** (12 layers)
   Each layer contains:
   - **Multi-Head Self-Attention** (12 heads)
   - **Feed-Forward Network** (4× hidden dimension)
   - **Layer Normalization** & **Residual Connections**

#### B. Multi-Head Self-Attention

```
Attention(Q,K,V) = softmax(QK^T / √d_k)V

Multi-Head(h_i) = Attention_i(Q,K,V)
MultiHead = Concat(h_1,...,h_n)W^O
```

**Process:**
1. Linear projections create Q (Query), K (Key), V (Value)
2. Compute attention weights: scale and normalize
3. Apply weights to values
4. Concatenate all heads
5. Final linear projection

**Purpose:** Allows model to attend to different parts of text simultaneously

#### C. Zero-Shot Classification Approach

**Premise**: Without fine-tuning, classify text using entailment scores

**Method**:
```
For each category:
  - Create hypothesis: "This text is about [category]"
  - Compute entailment score: P(text entails hypothesis)
  - Use score as category likelihood

Final Category = argmax(entailment scores)
```

**Advantages:**
- Works with any category labels (no retraining needed)
- Captures semantic relationships
- Understands complex linguistic patterns
- Better generalization

### Training & Configuration

**Pre-trained Model**: `facebook/bart-large-mnli`
- Parameters: 406M
- Training data: MNLI (Multi-Genre Natural Language Inference)
- Fine-tuned for entailment/contradiction classification

**Inference Configuration**:
- Device: GPU (mps:0 on Apple Silicon) or CPU
- Batch size: 1
- Processing speed: ~100-200ms per article (slower than Sklearn)
- Memory: ~3GB GPU/CPU

### Performance Characteristics

| Aspect | Score/Description |
|--------|------------------|
| Semantic Understanding | Excellent |
| Context Awareness | Very Good |
| Nuanced Classifications | Better than Sklearn |
| Processing Speed | Slower (~100-200ms) |
| Memory Usage | Higher (~3GB) |
| Few-Shot Learning | Supported |

### Advantages Over Naive Bayes

1. **Contextual Understanding**: Captures word relationships
2. **Semantic Knowledge**: Understands synonyms, antonyms
3. **Multi-layer Learning**: 12 encoder layers extract features
4. **Attention Mechanisms**: Focuses on relevant text parts
5. **Transfer Learning**: Pre-trained on 433M entailment examples

---

## 3. Model Comparison

### Feature Comparison

| Feature | Sklearn | Transformer |
|---------|---------|-------------|
| **Speed** | ⚡⚡⚡ Fast | ⚡ Slow |
| **Accuracy** | ⭐⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ Excellent |
| **Memory** | 💾 Low | 💾💾💾 High |
| **Interpretability** | 🔍 High | 🔍 Low |
| **Context** | Limited | Excellent |
| **Semantic** | Basic | Advanced |
| **Scalability** | Good | Limited |
| **Training Time** | Minutes | Hours |

### Use Cases

**Choose Sklearn when:**
- ✅ Speed is critical
- ✅ Running on limited hardware
- ✅ High volume predictions needed
- ✅ Interpretability matters
- ✅ Simple classification tasks

**Choose Transformer when:**
- ✅ Maximum accuracy needed
- ✅ Complex linguistic patterns matter
- ✅ Nuanced classifications required
- ✅ Few-shot learning needed
- ✅ GPU available

---

## 4. Dataset Information

### Data Sources

1. **AG News** (120,000 samples)
   - Business, Sports, Technology, Entertainment

2. **BBC News** (2,225 samples)
   - Tech, Business, Sport, Entertainment, Politics

3. **HuggingFace News Dataset** (2,225 samples)
   - Multiple categories

4. **Synthetic Data** (Generated)
   - Health, Science, World, Lifestyle, Education, Legal, Finance

### Data Processing

```
Raw Data (multiple sources)
    ↓
Deduplication (remove duplicates)
    ↓
Normalization (standardize categories)
    ↓
Cleaning (remove NaN, short texts)
    ↓
Length Filtering (50-15000 characters)
    ↓
Balancing (normalize category distribution)
    ↓
Final Dataset (120,577 samples, 12 categories)
```

### Final Dataset Statistics

| Metric | Value |
|--------|-------|
| **Total Samples** | 120,577 |
| **Training Samples** | 96,461 (80%) |
| **Test Samples** | 24,116 (20%) |
| **Total Categories** | 12 |
| **Avg. Text Length** | 200-500 tokens |
| **Vocabulary Size** | 1000 (TF-IDF) |

### Category Distribution

```
Business       : ~30,000 samples
Entertainment  : ~30,000 samples
Sports         : ~30,000 samples
Technology     : ~30,000 samples
Politics       : ~400 samples
Health         : ~50 samples
Science        : ~50 samples
World          : ~50 samples
Lifestyle      : ~50 samples
Education      : ~50 samples
Legal          : ~50 samples
Finance        : ~50 samples
```

---

## 5. Technical Implementation

### Dependencies

```python
# Core ML libraries
scikit-learn==1.7.2      # TF-IDF Vectorizer, Naive Bayes
transformers==4.46.2     # BART model
torch==2.5.1            # PyTorch backend
numpy==2.3.4            # Numerical computing
pandas==2.2.3           # Data manipulation
nltk==3.9.2             # Text preprocessing
```

### Model Loading

```python
# Sklearn Pipeline
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=1000, stop_words='english')),
    ('classifier', MultinomialNB())
])

# Transformer Model
from transformers import pipeline

transformer = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)
```

### Inference Pipeline

```python
# 1. Text Preprocessing
cleaned_text = preprocess(input_text)

# 2. Model Selection
if model_type == "sklearn":
    vectorized = tfidf_vectorizer.transform([cleaned_text])
    predictions = naive_bayes.predict_proba(vectorized)
else:
    predictions = transformer(cleaned_text, categories)

# 3. Post-processing
confidence_scores = normalize_probabilities(predictions)
final_category = argmax(confidence_scores)
```

---

## 6. Model Improvements & Future Work

### Current Limitations

1. **Sklearn Model**
   - Cannot understand semantic relationships
   - Word order independence assumption
   - Limited to training vocabulary

2. **Transformer Model**
   - Slow inference (not suitable for real-time)
   - High memory consumption
   - Requires GPU for practical speed

### Potential Improvements

1. **Model Ensemble**
   - Combine both models for better accuracy
   - Weighted voting based on confidence

2. **Fine-tuning**
   - Fine-tune BART on domain-specific data
   - Transfer learning on news classification

3. **Optimization**
   - Quantization for faster inference
   - Model distillation for smaller models
   - ONNX export for deployment

4. **Data Enhancement**
   - Add more training samples
   - Balance underrepresented categories
   - Add domain-specific vocabulary

5. **Advanced Techniques**
   - Multi-label classification
   - Hierarchical categories
   - Active learning for continuous improvement

---

## 7. API Integration

### Sklearn Endpoint

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Apple releases new iPhone with advanced AI features",
    "model_type": "sklearn"
  }'

Response:
{
  "category": "Technology",
  "confidence": 0.92,
  "confidence_scores": {
    "Technology": 0.92,
    "Business": 0.05,
    "Entertainment": 0.02,
    ...
  },
  "model_type": "sklearn",
  "processing_time": 0.008
}
```

### Transformer Endpoint

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Apple releases new iPhone with advanced AI features",
    "model_type": "transformer"
  }'

Response:
{
  "category": "Technology",
  "confidence": 0.98,
  "confidence_scores": {
    "Technology": 0.98,
    "Business": 0.01,
    "Science": 0.005,
    ...
  },
  "model_type": "transformer",
  "processing_time": 0.152
}
```

---

## Conclusion

The News Category Classifier provides two complementary models:

- **Sklearn**: Fast, efficient, interpretable - ideal for production systems
- **Transformer**: Accurate, semantic-aware - ideal for quality-critical applications

Users can choose based on their requirements for speed vs. accuracy, enabling flexibility across different use cases.
