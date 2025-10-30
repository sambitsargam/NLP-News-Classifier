#!/bin/bash

# News Category Classifier Setup Script
# This script sets up the entire project without Docker

set -e  # Exit on error

echo "🚀 News Category Classifier - Setup Script"
echo "==========================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "Please install Python 3.9 or higher from https://www.python.org"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Python $PYTHON_VERSION found"

# Check Node
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed"
    echo "Please install Node.js 16 or higher from https://nodejs.org"
    exit 1
fi

NODE_VERSION=$(node --version)
echo "✓ Node.js $NODE_VERSION found"

echo ""

# Setup Backend
echo "📦 Setting up Backend..."
cd backend
pip install -r requirements.txt
cd ..
echo "✓ Backend dependencies installed"

echo ""

# Download Data
echo "📥 Downloading Training Data..."
cd ml_model
python3 download_data.py
cd ..
echo "✓ Training data downloaded and saved"

echo ""

# Train Model
echo "🧠 Training ML Model..."
cd ml_model
python3 train.py
cd ..
echo "✓ Model trained and saved"

echo ""

# Setup Frontend
echo "🎨 Setting up Frontend..."
cd frontend
npm install
cd ..
echo "✓ Frontend dependencies installed"

echo ""
echo "==========================================="
echo "✅ Setup Complete!"
echo ""
echo "To start the application, open 2 terminals:"
echo ""
echo "Terminal 1 - Backend:"
echo "  cd backend"
echo "  python main.py"
echo ""
echo "Terminal 2 - Frontend:"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Then open your browser to: http://localhost:5173"
echo ""
echo "API Documentation: http://localhost:8000/docs"
echo "==========================================="
