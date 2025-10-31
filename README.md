# News Category Classifier

A full-stack web application for automatic news article classification using Natural Language Processing (NLP) and Machine Learning.

## 📋 Overview

This project automatically classifies news articles into predefined categories (Sports, Politics, Technology, Entertainment, Business, Health, Science) using machine learning models. It provides a clean, user-friendly interface for uploading or entering news text with instant predictions and confidence scores.

## 🎯 Features

- **Text Input & File Upload** - Paste articles or upload text files for classification
- **Multi-Model Support** - Choose between fast Sklearn or accurate Transformer models
- **Confidence Scores** - See detailed confidence metrics for each category
- **Real-time Predictions** - Get instant classification results
- **Beautiful UI** - Modern, responsive web interface
- **REST API** - Full-featured API for programmatic access
- **Batch Processing** - Classify multiple articles at once

## 🏗️ Project Structure

```
NLP-News-Classifier/
├── backend/                 # FastAPI backend service
│   ├── main.py             # Main FastAPI application
│   ├── model_service.py    # ML model inference service
│   ├── utils.py            # Text preprocessing utilities
│   ├── requirements.txt    # Python dependencies
│   └── .env.example        # Environment configuration template
├── frontend/               # React frontend application
│   ├── src/
│   │   ├── App.jsx         # Main React component
│   │   ├── api.js          # API client
│   │   ├── components/     # React components
│   │   │   ├── PredictionForm.jsx
│   │   │   └── ResultDisplay.jsx
│   │   └── index.css       # Global styles
│   ├── package.json        # Node dependencies
│   └── vite.config.js      # Vite configuration
├── ml_model/               # Machine learning model
│   ├── train.py           # Model training script
│   └── models/            # Trained model storage
├── data/                   # Data storage
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 16+
- npm or yarn

### Installation & Setup

#### 1. Clone Repository
```bash
git clone https://github.com/sambitsargam/NLP-News-Classifier.git
cd NLP-News-Classifier
```

#### 2. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

#### 2. Download Training Data

```bash
cd ml_model
python3 download_data.py
cd ..
```

This will download and prepare news data in the `data/` folder:
- `data/news_data.csv` - Training data in CSV format
- `data/news_data.json` - Training data in JSON format
- `data/data_summary.txt` - Dataset statistics

#### 3. Train the Model

```bash
cd ml_model
python3 train.py
cd ..
```

This will create a trained model in `ml_model/models/`. The training automatically uses the downloaded data.

#### 4. Start Backend Server

```bash
cd ../backend
python main.py
```

The API will be available at `http://localhost:8000`

**API Documentation**: http://localhost:8000/docs

#### 5. Install & Start Frontend

```bash
cd ../frontend
npm install
npm run dev
```

The web app will be available at `http://localhost:5173`

## 📚 API Endpoints

### Health Check
```
GET /health
```

### Predict Category
```
POST /predict
Content-Type: application/json

{
  "text": "Your news article text here",
  "model_type": "sklearn"
}
```

### Predict from File
```
POST /predict-file
Content-Type: multipart/form-data

file: <text-file>
```

### Get Available Categories
```
GET /categories
```

### Batch Predict
```
POST /batch-predict
Content-Type: application/json

[
  {"text": "Article 1", "model_type": "sklearn"},
  {"text": "Article 2", "model_type": "sklearn"}
]
```

For detailed API documentation, see [API.md](API.md)

## 📊 Supported Categories

1. **Sports** - Sports news, games, athletes
2. **Politics** - Political news, elections, government
3. **Technology** - Tech news, software, gadgets
4. **Entertainment** - Movies, music, celebrities
5. **Business** - Business news, stocks, economy
6. **Health** - Health news, medical research
7. **Science** - Science discoveries, research

## 🧠 Model Details

### Sklearn Model
- **Algorithm**: TF-IDF + Multinomial Naive Bayes
- **Speed**: Very fast (< 50ms)
- **Accuracy**: Good for most use cases

### Transformer Model
- **Algorithm**: BART Large MNLI (Zero-shot classification)
- **Speed**: Slower but more accurate (200-500ms)
- **Accuracy**: Excellent for nuanced classification

**For detailed algorithm documentation, metrics, and technical details, see [MODEL.md](MODEL.md)**

This comprehensive guide includes:
- Complete mathematical formulations
- Architecture diagrams
- Performance comparisons
- Dataset information
- Training procedures
- API integration examples

## 🔧 Configuration

```

Create a `.env` file in the backend directory:

```env
FLASK_ENV=development
DEBUG=True
MODEL_TYPE=sklearn
LOG_LEVEL=INFO
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

## 📝 Training Custom Model

To train the model with your own data:

1. Prepare a CSV file with columns: `text`, `category`
2. Update `ml_model/train.py` to load your data
3. Run: `python ml_model/train.py`

Example CSV format:
```csv
text,category
"Breaking news about the championship game",Sports
"New tech startup raises millions",Technology
```

See [ml_model/README.md](ml_model/README.md) for more details.

## 🎯 Extending the Project

### Add New Categories
1. Update `CATEGORIES` in `backend/model_service.py`
2. Retrain the model with new category examples
3. Restart the backend

### Use Custom Model
1. Train your model and save it as joblib files
2. Place in `ml_model/models/`
3. Update `model_service.py` to load your model

## 📈 Performance Optimization

- **Caching**: Add Redis for prediction caching
- **Batching**: Process multiple articles efficiently
- **Model Optimization**: Use ONNX for faster inference
- **Load Balancing**: Deploy multiple backend instances

## 🔐 Security Considerations

- Add authentication and authorization
- Implement rate limiting
- Validate and sanitize inputs
- Use HTTPS in production
- Add CSRF protection

## 🐛 Troubleshooting

### Backend won't start
- Check if port 8000 is in use: `lsof -i :8000`
- Ensure all dependencies installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.9+)

### Frontend connection issues
- Check if backend is running on port 8000
- Verify CORS is enabled in backend
- Check browser console for detailed errors

### Model not loaded
- Run training script: `python ml_model/train.py`
- Check `ml_model/models/` directory exists
- Verify model files are created

### Low prediction accuracy
- Provide more diverse training data
- Try the transformer model
- Check text preprocessing doesn't remove important info

## 🚀 Deployment

### Local Deployment

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Production Build

**Frontend:**
```bash
cd frontend
npm run build
# Outputs to frontend/dist/
```

**Backend:**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👥 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review documentation

## 🚀 Future Enhancements

- [ ] Multilingual support
- [ ] Real-time news scraping
- [ ] Model explainability (SHAP/LIME)
- [ ] User feedback system for model improvement
- [ ] Visualization dashboard
- [ ] Advanced analytics
- [ ] Custom category support
- [ ] Model versioning system

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev)
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [NLTK Documentation](https://www.nltk.org/)
- [Hugging Face Transformers](https://huggingface.co/transformers/)

---

**Built with ❤️ for automatic news classification**