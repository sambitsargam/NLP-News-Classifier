# How to Run the News Category Classifier

Quick setup and running guide with all necessary commands.

## Prerequisites

- Python 3.11+
- Node.js 16+
- npm or yarn
- ~4GB RAM (8GB+ recommended for transformer model)
- GPU (optional, but recommended for transformer model)

---

## 1. Clone & Navigate to Project

```bash
cd /Users/sambit/Desktop/NLP-News-Classifier
```

Or if not yet cloned:
```bash
git clone https://github.com/sambitsargam/NLP-News-Classifier.git
cd NLP-News-Classifier
```

---

## 2. Create Python Virtual Environment

```bash
# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate

# On Windows use:
# venv\Scripts\activate
```

---

## 3. Install Python Dependencies

```bash
cd backend
pip install --upgrade pip
pip install -r requirements.txt
```

### If requirements.txt is missing, install manually:

```bash
pip install fastapi==0.109.0
pip install uvicorn==0.27.0
pip install scikit-learn==1.7.2
pip install nltk==3.9.2
pip install numpy==2.3.4
pip install pydantic==2.5.0
pip install pydantic-settings==2.1.0
pip install python-multipart==0.0.6
pip install python-dotenv==1.0.0
pip install transformers==4.46.2
pip install torch==2.5.1
pip install pandas==2.2.3
```

---

## 4. Download and Prepare Data

```bash
cd ../ml_model

# Download datasets from online sources
python3.11 download_comprehensive_data.py

# Augment dataset with synthetic data (to reach 12 categories)
python3.11 augment_data.py

# Generate synthetic data for underrepresented categories
python3.11 generate_synthetic.py

# Balance the dataset
python3.11 balance_data.py
```

---

## 5. Train Machine Learning Model

```bash
cd ../ml_model

# Train the model with 120K+ samples and 12 categories
python3.11 train.py

# Expected output:
# INFO:__main__:Model trained with accuracy: 0.85
# INFO:__main__:✓ Model saved to models/
# INFO:__main__:✓ Training completed successfully!
```

---

## 6. Start Backend Server

### Option A: Using Uvicorn (Recommended)

```bash
cd ../backend

# Start backend on port 8000
python3.11 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Output should show:
# INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Option B: Direct Python

```bash
cd ../backend
python3.11 main.py
```

### Verify Backend is Running

```bash
# In a new terminal
curl http://localhost:8000/health

# Should return:
# {"status":"healthy","model_loaded":true,"sklearn_model_loaded":true,...}
```

---

## 7. Install Frontend Dependencies

### In a new terminal:

```bash
cd /Users/sambit/Desktop/NLP-News-Classifier/frontend

# Install npm packages
npm install

# Or with yarn:
# yarn install
```

---

## 8. Start Frontend Development Server

```bash
cd frontend

# Start Vite development server
npm run dev

# Or with yarn:
# yarn dev

# Output should show:
# ➜  Local:   http://localhost:5173/
# ➜  Network: use --host to expose
```

---

## 9. Open in Browser

```bash
# Automatically opens, or manually visit:
http://localhost:5173
```

---

## Full Running Setup (All in One)

### Terminal 1: Backend

```bash
cd /Users/sambit/Desktop/NLP-News-Classifier
source venv/bin/activate
cd backend
python3.11 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Terminal 2: Frontend

```bash
cd /Users/sambit/Desktop/NLP-News-Classifier/frontend
npm run dev
```

### Terminal 3: (Optional) Monitor Logs

```bash
cd /Users/sambit/Desktop/NLP-News-Classifier
tail -f backend.log
```

---

## Quick Commands Summary

| Command | Purpose |
|---------|---------|
| `source venv/bin/activate` | Activate Python environment |
| `pip install -r requirements.txt` | Install dependencies |
| `python3.11 download_comprehensive_data.py` | Download datasets |
| `python3.11 train.py` | Train ML model |
| `python3.11 -m uvicorn main:app --host 0.0.0.0 --port 8000` | Start backend |
| `npm install` | Install Node packages |
| `npm run dev` | Start frontend dev server |
| `curl http://localhost:8000/health` | Check backend health |
| `npm run build` | Build frontend for production |

---

## Environment Variables

### Create `.env` file in backend directory:

```bash
cd backend
cat > .env << 'EOF'
# Backend Configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]

# Model Configuration
MODEL_TYPE=both  # 'sklearn', 'transformer', or 'both'
USE_GPU=true
DEVICE=cuda  # or 'cpu', 'mps' (for Apple Silicon)

# API Configuration
MAX_TEXT_LENGTH=10000
BATCH_SIZE=32
EOF
```

---

## API Testing Commands

### Test Health Endpoint

```bash
curl http://localhost:8000/health
```

### Test Prediction (Sklearn)

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Apple releases new iPhone with advanced AI features",
    "model_type": "sklearn"
  }'
```

### Test Prediction (Transformer)

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Apple releases new iPhone with advanced AI features",
    "model_type": "transformer"
  }'
```

### Get Available Categories

```bash
curl http://localhost:8000/categories
```

### Batch Predict

```bash
curl -X POST http://localhost:8000/batch-predict \
  -H "Content-Type: application/json" \
  -d '{
    "texts": [
      "Stock market reaches all-time high",
      "New movie premiere sets box office records",
      "Scientists discover new particle"
    ]
  }'
```

### Upload and Predict File

```bash
curl -X POST http://localhost:8000/predict-file \
  -F "file=@path/to/article.txt" \
  -F "model_type=sklearn"
```

---

## Docker Setup (Optional)

### Build Docker Image

```bash
docker build -t news-classifier .
```

### Run with Docker

```bash
docker run -p 8000:8000 -p 5173:5173 news-classifier
```

---

## Production Deployment

### Frontend Build

```bash
cd frontend
npm run build
# Creates: dist/ folder with optimized build
```

### Backend Production

```bash
cd backend
python3.11 -m uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Using Gunicorn (ASGI)

```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

---

## Troubleshooting

### Port Already in Use

```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 5173
lsof -ti:5173 | xargs kill -9
```

### Python Virtual Environment Issues

```bash
# Remove and recreate venv
rm -rf venv
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Model Not Loading

```bash
# Retrain model
cd ml_model
python3.11 train.py

# Check model files exist
ls -la models/
```

### Frontend Not Connecting to Backend

```bash
# Check backend is running
curl http://localhost:8000/health

# Check CORS configuration in backend/main.py
# Verify frontend API URL is correct
```

### NPM Dependencies Issues

```bash
# Clear npm cache
npm cache clean --force

# Remove node_modules
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

---

## Verify Everything is Working

### 1. Check Backend Health

```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy",...}
```

### 2. Check Models Loaded

```bash
curl http://localhost:8000/model-info
# Should show both models loaded
```

### 3. Test a Prediction

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"Technology news about AI","model_type":"sklearn"}'
# Should return classification with category
```

### 4. Open Frontend

```bash
# Visit http://localhost:5173 in browser
# Should see the UI with all 12 categories
```

---

## Performance Notes

### Sklearn Model
- Memory: ~50MB
- Speed: ~5-10ms per prediction
- GPU: Not needed
- Best for: Real-time, high-throughput applications

### Transformer Model
- Memory: ~3GB
- Speed: ~100-200ms per prediction
- GPU: Recommended (Apple Silicon, NVIDIA, etc.)
- Best for: Maximum accuracy requirements

---

## File Locations

```
Project Root:           /Users/sambit/Desktop/NLP-News-Classifier
Backend:               ./backend/main.py
Frontend:              ./frontend/src/App.jsx
Models (Trained):      ./ml_model/models/
Dataset:               ./data/news_data_combined.csv
Logs:                  ./logs/ (if enabled)
Config:                ./backend/.env
```

---

## Next Steps

1. ✅ Run backend: `python3.11 -m uvicorn main:app --host 0.0.0.0 --port 8000`
2. ✅ Run frontend: `npm run dev`
3. ✅ Open browser: `http://localhost:5173`
4. ✅ Try predictions with both models
5. ✅ Read [MODEL.md](MODEL.md) for technical details
6. ✅ See [ALGORITHM_COMPARISON.md](ALGORITHM_COMPARISON.md) for model comparison

---

## Quick Command Reference

```bash
# Complete setup from scratch
cd /Users/sambit/Desktop/NLP-News-Classifier
source venv/bin/activate
cd backend && pip install -r requirements.txt

# Terminal 1: Start backend
cd backend
python3.11 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Start frontend
cd frontend
npm run dev

# Terminal 3: Test API
curl http://localhost:8000/health
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d '{"text":"Sample news text","model_type":"sklearn"}'
```

---

## Support

- Backend API docs: `http://localhost:8000/docs`
- Interactive API: `http://localhost:8000/redoc`
- Frontend: `http://localhost:5173`
- See [README.md](README.md) for more details
- See [MODEL.md](MODEL.md) for algorithm documentation
