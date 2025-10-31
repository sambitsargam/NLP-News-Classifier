# 📚 Documentation Guide

Welcome to the News Category Classifier documentation! Here's a guide to all available resources.

## 📄 Main Documentation Files

### 1. **[README.md](README.md)** - Start Here! 🚀
The main project documentation covering:
- Project overview and features
- Installation and setup instructions
- Quick start guide
- API endpoints reference
- Supported categories
- Troubleshooting guide
- How to extend the project

**Read this first** if you're new to the project.

---

### 2. **[MODEL.md](MODEL.md)** - Deep Technical Details 🧠
Comprehensive documentation of both machine learning models:
- **Sklearn Model**
  - TF-IDF vectorization explained
  - Multinomial Naive Bayes algorithm
  - Mathematical formulations
  - Performance metrics
  
- **Transformer Model**
  - BART architecture details
  - Multi-head attention mechanism
  - Zero-shot classification approach
  - Pre-training information

- **Dataset Information**
  - Data sources and collection
  - Processing pipeline
  - Category distribution
  - Training statistics

- **Implementation Details**
  - Dependencies and imports
  - Model loading procedures
  - Inference pipeline
  - API integration examples

**Read this** if you want to understand the algorithms in depth.

---

### 3. **[ALGORITHM_COMPARISON.md](ALGORITHM_COMPARISON.md)** - Quick Reference 📊
Side-by-side comparison and quick reference guide:
- Visual architecture diagrams for both models
- When to use each model
- Performance metrics comparison
- API usage examples
- Category support matrix
- Dataset statistics overview

**Read this** for quick decision-making and comparisons.

---

### 4. **[DATASET_INFO.md](DATASET_INFO.md)** - Data Details 📈
Detailed information about the training dataset:
- Data sources (AG News, BBC, HuggingFace)
- Collection methodology
- Preprocessing steps
- Category distribution
- Data statistics and analysis

**Read this** if you want to understand the dataset.

---

### 5. **[SETUP_COMPLETE.md](SETUP_COMPLETE.md)** - Setup Confirmation ✅
Checklist of all completed setup steps and components.

---

## 🎯 Quick Navigation by Use Case

### I want to...

#### **...get started quickly** 
→ Read [README.md](README.md) → Installation & Setup section

#### **...understand the algorithms**
→ Read [MODEL.md](MODEL.md) → Algorithm Details sections

#### **...compare the two models**
→ Read [ALGORITHM_COMPARISON.md](ALGORITHM_COMPARISON.md)

#### **...integrate the API**
→ Read [README.md](README.md) → API Endpoints section
→ Or [MODEL.md](MODEL.md) → API Integration section

#### **...understand the dataset**
→ Read [DATASET_INFO.md](DATASET_INFO.md)
→ Or [MODEL.md](MODEL.md) → Dataset Information section

#### **...troubleshoot issues**
→ Read [README.md](README.md) → Troubleshooting section

#### **...extend the project**
→ Read [README.md](README.md) → Extending the Project section

---

## 📊 Models Overview

### Two Models Available

#### 1️⃣ **Sklearn Model** (Fast & Efficient)
- **Algorithm**: TF-IDF + Multinomial Naive Bayes
- **Speed**: ⚡ ~5-10ms per prediction
- **Accuracy**: ⭐⭐⭐⭐ 85%
- **Memory**: 💾 ~50MB
- **GPU**: ❌ Not needed
- **Best for**: Production systems, real-time predictions
- **Documentation**: See MODEL.md § 1

#### 2️⃣ **Transformer Model** (Accurate & Semantic)
- **Algorithm**: BART-based Zero-Shot Classification
- **Speed**: 🐢 ~100-200ms per prediction
- **Accuracy**: ⭐⭐⭐⭐⭐ 94%+
- **Memory**: 💾💾💾 ~3GB
- **GPU**: ✅ Recommended
- **Best for**: Accuracy-critical applications
- **Documentation**: See MODEL.md § 2

---

## 📋 Supported Categories (12)

The classifier supports these news categories:

| Category | Icon | Examples |
|----------|------|----------|
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

## 🗂️ Project Structure

```
NLP-News-Classifier/
├── README.md                      # Main documentation
├── MODEL.md                       # Algorithm details
├── ALGORITHM_COMPARISON.md        # Quick reference
├── DATASET_INFO.md               # Dataset details
├── DOCUMENTATION.md              # This file
│
├── backend/
│   ├── main.py                  # FastAPI server
│   ├── model_service.py         # ML inference
│   ├── utils.py                 # Text utilities
│   └── requirements.txt          # Python deps
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # Main React component
│   │   ├── api.js               # API client
│   │   └── components/          # React components
│   ├── package.json             # Node deps
│   └── vite.config.js           # Vite config
│
├── ml_model/
│   ├── train.py                 # Training script
│   ├── download_*.py            # Data download scripts
│   └── models/                  # Trained models
│
└── data/
    └── news_data_combined.csv   # Training dataset
```

---

## 🚀 Quick Start Commands

### Backend Setup
```bash
cd backend
python3.11 -m pip install -r requirements.txt
python3.11 -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Open in Browser
```
http://localhost:5173
```

---

## 📚 Learning Path Recommendations

### For Beginners:
1. Read [README.md](README.md) - Get oriented
2. Run the Quick Start - Get it working
3. Try making predictions in the UI
4. Read [ALGORITHM_COMPARISON.md](ALGORITHM_COMPARISON.md) - Understand the differences

### For ML/NLP Engineers:
1. Read [MODEL.md](MODEL.md) - Understand the algorithms
2. Review [DATASET_INFO.md](DATASET_INFO.md) - Understand the data
3. Check source code: `backend/model_service.py`
4. Review `ml_model/train.py` - Training pipeline

### For DevOps/Backend Engineers:
1. Read [README.md](README.md) - Project overview
2. Check [README.md](README.md) - API Endpoints section
3. Review `backend/main.py` - FastAPI implementation
4. Set up Docker if needed

### For Frontend Engineers:
1. Read [README.md](README.md) - Features overview
2. Review `frontend/src/App.jsx` - React implementation
3. Check `frontend/src/api.js` - API client
4. Check CSS files for styling

---

## 🔍 Key Concepts Explained

### TF-IDF (Term Frequency-Inverse Document Frequency)
Converts text into numerical vectors by:
- Counting how often words appear in a document
- Weighting by how rare/common words are across all documents
- See [MODEL.md](MODEL.md) § 1.A for details

### Naive Bayes
Probabilistic classifier that:
- Learns category probabilities from training data
- Predicts based on word frequency statistics
- Assumes word independence (simplified assumption)
- See [MODEL.md](MODEL.md) § 1.B for details

### BART Transformer
Neural network model that:
- Uses 12 layers of self-attention
- Understands semantic relationships
- Learned from 433M entailment examples
- Can classify without task-specific training
- See [MODEL.md](MODEL.md) § 2 for details

### Zero-Shot Classification
Technique that:
- Classifies into ANY categories without retraining
- Uses entailment scoring between text and categories
- Enables generalization to new categories
- See [MODEL.md](MODEL.md) § 2.C for details

---

## ❓ Common Questions

**Q: Which model should I use?**
A: See [ALGORITHM_COMPARISON.md](ALGORITHM_COMPARISON.md) § "When to use each model"

**Q: How accurate is the classifier?**
A: Sklearn: 85%, Transformer: 94%+. See [MODEL.md](MODEL.md) § Performance Metrics

**Q: Can I use custom categories?**
A: Yes, the Transformer model supports any categories. See [README.md](README.md) § Extending

**Q: How fast is it?**
A: Sklearn: 5-10ms, Transformer: 100-200ms per article

**Q: What's the dataset size?**
A: 120,577 articles across 12 categories. See [DATASET_INFO.md](DATASET_INFO.md)

**Q: How do I train a custom model?**
A: See [README.md](README.md) § Training Custom Model

---

## 🤝 Contributing

To improve documentation:
1. Edit the relevant `.md` file
2. Keep formatting consistent
3. Add examples where helpful
4. Update cross-references
5. Submit pull request

---

## 📞 Support

For issues or questions:
1. Check [README.md](README.md) § Troubleshooting
2. Review relevant documentation file
3. Check source code comments
4. Open an issue on GitHub

---

**Last Updated:** October 31, 2025
**Model Version:** 2.0
**Dataset Version:** 1.2
