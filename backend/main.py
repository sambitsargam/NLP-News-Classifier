"""
FastAPI Backend for News Category Classifier
Provides REST API endpoints for news classification
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging
from model_service import NewsClassifierService
from utils import preprocess_text, generate_confidence_dict
import os
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="News Category Classifier API",
    description="API for automatic news article classification using NLP",
    version="1.0.0"
)

# Configure CORS
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the classifier service
classifier_service = None


# Pydantic models
class ArticleInput(BaseModel):
    """Model for article text input"""
    text: str
    model_type: Optional[str] = "sklearn"  # "sklearn" or "transformer"


class PredictionResponse(BaseModel):
    """Model for prediction response"""
    category: str
    confidence: float
    confidence_scores: Dict[str, float]
    input_text: str
    processing_time: float


class HealthResponse(BaseModel):
    """Model for health check response"""
    status: str
    model_loaded: bool
    available_models: list


@app.on_event("startup")
async def startup_event():
    """Initialize the classifier service on startup"""
    global classifier_service
    try:
        classifier_service = NewsClassifierService()
        logger.info("Classifier service initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize classifier service: {e}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down News Classifier API")


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy" if classifier_service else "unhealthy",
        model_loaded=classifier_service is not None,
        available_models=["sklearn", "transformer"]
    )


@app.post("/predict", response_model=PredictionResponse)
async def predict_category(article: ArticleInput):
    """
    Predict the category of a news article
    
    Args:
        article: ArticleInput containing text and optional model_type
        
    Returns:
        PredictionResponse with predicted category and confidence scores
    """
    if not classifier_service:
        raise HTTPException(status_code=503, detail="Classifier service not initialized")
    
    if not article.text or len(article.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Article text cannot be empty")
    
    try:
        # Preprocess the text
        processed_text = preprocess_text(article.text)
        
        # Get prediction
        result = classifier_service.predict(
            processed_text,
            model_type=article.model_type
        )
        
        return PredictionResponse(
            category=result["category"],
            confidence=result["confidence"],
            confidence_scores=result["confidence_scores"],
            input_text=article.text[:100] + "..." if len(article.text) > 100 else article.text,
            processing_time=result["processing_time"]
        )
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.post("/predict-file")
async def predict_from_file(file: UploadFile = File(...)):
    """
    Predict category from uploaded text file
    
    Args:
        file: Text file containing news article
        
    Returns:
        PredictionResponse with predicted category
    """
    if not classifier_service:
        raise HTTPException(status_code=503, detail="Classifier service not initialized")
    
    try:
        content = await file.read()
        text = content.decode("utf-8")
        
        if not text or len(text.strip()) == 0:
            raise HTTPException(status_code=400, detail="File is empty")
        
        # Preprocess and predict
        processed_text = preprocess_text(text)
        result = classifier_service.predict(processed_text)
        
        return PredictionResponse(
            category=result["category"],
            confidence=result["confidence"],
            confidence_scores=result["confidence_scores"],
            input_text=text[:100] + "..." if len(text) > 100 else text,
            processing_time=result["processing_time"]
        )
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be valid UTF-8 text")
    except Exception as e:
        logger.error(f"File prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"File processing failed: {str(e)}")


@app.get("/categories")
async def get_available_categories():
    """Get list of available news categories"""
    if not classifier_service:
        raise HTTPException(status_code=503, detail="Classifier service not initialized")
    
    return {
        "categories": classifier_service.get_categories(),
        "total_categories": len(classifier_service.get_categories())
    }


@app.get("/model-info")
async def get_model_info():
    """Get information about the loaded model"""
    if not classifier_service:
        raise HTTPException(status_code=503, detail="Classifier service not initialized")
    
    return classifier_service.get_model_info()


@app.post("/batch-predict")
async def batch_predict(articles: list[ArticleInput]):
    """
    Predict categories for multiple articles
    
    Args:
        articles: List of ArticleInput objects
        
    Returns:
        List of PredictionResponse objects
    """
    if not classifier_service:
        raise HTTPException(status_code=503, detail="Classifier service not initialized")
    
    if len(articles) > 100:
        raise HTTPException(status_code=400, detail="Maximum 100 articles per request")
    
    results = []
    for article in articles:
        try:
            processed_text = preprocess_text(article.text)
            result = classifier_service.predict(processed_text, model_type=article.model_type)
            
            results.append(PredictionResponse(
                category=result["category"],
                confidence=result["confidence"],
                confidence_scores=result["confidence_scores"],
                input_text=article.text[:100] + "..." if len(article.text) > 100 else article.text,
                processing_time=result["processing_time"]
            ))
        except Exception as e:
            logger.error(f"Batch prediction error: {e}")
            results.append({
                "error": str(e),
                "text": article.text[:100] + "..."
            })
    
    return {"predictions": results, "total": len(results), "successful": len([r for r in results if "error" not in r])}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True
    )
