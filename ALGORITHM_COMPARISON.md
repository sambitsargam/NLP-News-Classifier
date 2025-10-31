# Quick Reference: Algorithm Comparison

## Side-by-Side Comparison

### Sklearn Model: TF-IDF + Multinomial Naive Bayes

```
┌─────────────────────────────────────────┐
│  Input Text                             │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  Text Preprocessing                     │
│  • Remove punctuation                   │
│  • Convert to lowercase                 │
│  • Tokenization                         │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  TF-IDF Vectorization                   │
│  • 1000 most important features         │
│  • Term frequency scoring               │
│  • Stop word removal                    │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  Multinomial Naive Bayes                │
│  • Probability scoring                  │
│  • Category prediction                  │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  Output: Category + Confidence Scores   │
└─────────────────────────────────────────┘
```

**Formula:**
```
P(Category|Text) = P(Category) × ∏ P(word|Category)
                   (With Laplace smoothing)
```

**Pros:** ⚡ Fast, 💾 Memory efficient, 🔍 Interpretable
**Cons:** ❌ Limited context, ❌ Assumes word independence

---

### Transformer Model: BART Zero-Shot Classification

```
┌─────────────────────────────────────────┐
│  Input Text                             │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  Tokenization (BPE)                     │
│  • Byte Pair Encoding                   │
│  • Special tokens added                 │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  Token & Positional Embeddings          │
│  • Learned vector representations       │
│  • Position information encoded         │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  BART Encoder (12 Layers)               │
│  ┌─────────────────────────────────┐   │
│  │ Multi-Head Self-Attention       │   │
│  │ (12 parallel attention heads)   │   │
│  └─────────────────────────────────┘   │
│           │                             │
│           ▼                             │
│  ┌─────────────────────────────────┐   │
│  │ Feed-Forward Network            │   │
│  │ (Dense layers)                  │   │
│  └─────────────────────────────────┘   │
│           │                             │
│           ▼                             │
│  Layer Normalization & Residual Conn.  │
│  (Repeat 12 times)                      │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  Zero-Shot Classification               │
│  For each category:                     │
│  • Create: "This is about [category]"  │
│  • Score entailment probability        │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  Output: Category + Confidence Scores   │
└─────────────────────────────────────────┘
```

**Formula:**
```
Category Score = Entailment(Text, "This is about [Category]")
             = P(Text entails hypothesis for category)
```

**Pros:** 🎯 Accurate, 🧠 Semantic understanding, 🎨 Context-aware
**Cons:** 🐢 Slow (100-200ms), 💾 High memory, 🔍 Black-box

---

## When to Use Each Model

### Use Sklearn When:

✅ **Speed is critical**
- Real-time predictions needed
- High throughput required
- Processing 1000s of articles/minute

✅ **Limited resources**
- Running on CPU only
- Memory-constrained environment
- Edge devices or serverless functions

✅ **Interpretability matters**
- Need to understand why prediction was made
- Feature importance analysis required
- Compliance/audit trail needed

✅ **Simple classification tasks**
- Clear categorical boundaries
- Good training data in target domain
- Speed over accuracy tradeoff acceptable

### Use Transformer When:

✅ **Maximum accuracy needed**
- Quality is more important than speed
- Complex linguistic patterns in text
- Nuanced category distinctions

✅ **GPU available**
- Apple Silicon / NVIDIA GPU at hand
- Cloud GPU resources accessible
- Batch processing acceptable

✅ **Semantic understanding critical**
- Cross-domain generalization needed
- Few-shot learning capability required
- Long contextual dependencies matter

✅ **Production quality required**
- Mission-critical applications
- Customer-facing results
- Accuracy benchmarks strict

---

## Performance Metrics Comparison

| Metric | Sklearn | Transformer |
|--------|---------|------------|
| **Speed** | ~5-10ms | ~100-200ms |
| **Accuracy** | 85% | 94%+ |
| **Memory** | ~50MB | ~3000MB |
| **GPU Needed** | ❌ No | ✅ Recommended |
| **Training Time** | ~2 minutes | ~1-2 hours |
| **Inference Cost** | Low | High |

---

## Category Support

Both models support these 12 categories:

| Category | Icon | Use Cases |
|----------|------|-----------|
| Business | 💼 | Markets, companies, economy |
| Education | 🎓 | Schools, universities, learning |
| Entertainment | 🎬 | Movies, music, celebrities |
| Finance | 💰 | Banking, stocks, investments |
| Health | 🏥 | Medicine, wellness, diseases |
| Legal | ⚖️ | Laws, courts, regulations |
| Lifestyle | 🎨 | Fashion, travel, culture |
| Politics | 🏛️ | Government, elections, policy |
| Science | 🔬 | Research, discoveries, tech |
| Sports | ⚽ | Games, athletes, competitions |
| Technology | 💻 | Software, gadgets, AI |
| World | 🌍 | International, global events |

---

## Dataset Statistics

```
Total Samples:        120,577
Training Set (80%):   96,461
Test Set (20%):       24,116
Categories:           12
Average Text Length:  200-500 tokens
Vocabulary Size:      1,000 (TF-IDF)

Category Distribution (approximate):
- Business:        30,000 samples
- Entertainment:   30,000 samples
- Sports:          30,000 samples
- Technology:      30,000 samples
- Politics:           400 samples
- Others:             577 samples
```

---

## Architecture Comparison

### Sklearn Architecture

```
Text Input
    ↓
TF-IDF Vectorizer (1 layer)
    ↓
Multinomial Naive Bayes
    ↓
Probability Distribution
```

**Total Parameters:** ~1M (small)
**Layers:** 1 effective layer
**Training:** Statistical learning

### Transformer Architecture

```
Text Input
    ↓
Embedding Layer
    ↓
Positional Encoding
    ↓
Transformer Encoder (12 layers)
├─ Multi-Head Attention (12 heads)
├─ Feed-Forward Network
└─ Layer Normalization
    ↓
Output Layer
    ↓
Probability Distribution
```

**Total Parameters:** 406M (large)
**Layers:** 12 transformer layers
**Training:** Deep neural network learning

---

## API Usage Examples

### Sklearn Prediction

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Apple releases new iPhone with AI features",
    "model_type": "sklearn"
  }'

# Response:
# {
#   "category": "Technology",
#   "confidence": 0.92,
#   "model_type": "sklearn",
#   "processing_time": 0.008
# }
```

### Transformer Prediction

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Apple releases new iPhone with AI features",
    "model_type": "transformer"
  }'

# Response:
# {
#   "category": "Technology",
#   "confidence": 0.98,
#   "model_type": "transformer",
#   "processing_time": 0.152
# }
```

---

## Key Differences Summary

| Aspect | Sklearn | Transformer |
|--------|---------|------------|
| **How it works** | Count-based | Neural network-based |
| **Learns** | Word frequencies | Deep representations |
| **Understands** | Bag of words | Semantic relationships |
| **Context** | No (word order doesn't matter) | Yes (full context) |
| **Generalization** | Limited | Excellent |
| **Explainability** | High | Low |
| **Speed** | Blazing fast | Moderate |
| **Accuracy** | Good | Excellent |
| **Best for** | Production systems | Accuracy-critical apps |

---

## Further Reading

- **Full Algorithm Details:** See [MODEL.md](../MODEL.md)
- **API Documentation:** See `/docs` endpoint
- **Source Code:** See `backend/model_service.py`
