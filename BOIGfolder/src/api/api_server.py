from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
import uvicorn
from typing import List, Optional
import os
import sys
import logging

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

try:
    from ml.simple_pipeline import SimplePipeline
except ImportError:
    SimplePipeline = None

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Big Data Land Price API", 
    version="1.0.0",
    description="AI-powered land price prediction API"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ML pipeline
try:
    ml_pipeline = SimplePipeline() if SimplePipeline else None
except Exception as e:
    logger.error(f"Failed to initialize ML pipeline: {e}")
    ml_pipeline = None

class PropertyRequest(BaseModel):
    city: str
    area: int
    road_width: int
    distance_from_city: int
    property_type: str
    amenities: List[str] = []
    location: Optional[str] = "Central"
    
    @validator('area')
    def validate_area(cls, v):
        if v < 100 or v > 50000:
            raise ValueError('Area must be between 100 and 50000 sq ft')
        return v
    
    @validator('city')
    def validate_city(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('City cannot be empty')
        return v.strip()

class PropertyResponse(BaseModel):
    predicted_price: float
    price_per_sqft: float
    city: str
    area: int
    confidence: str

@app.get("/")
async def root():
    return {"message": "Big Data Land Price API", "status": "active"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "data_status": "available",
        "total_records": 100000,
        "model_status": "active",
        "api_version": "1.0.0"
    }

@app.post("/predict", response_model=PropertyResponse)
async def predict_price(request: PropertyRequest):
    try:
        if not ml_pipeline:
            raise HTTPException(status_code=503, detail="ML pipeline not available")
        
        # Use ML pipeline for prediction
        result = ml_pipeline.predict_price(
            city=request.city,
            area=request.area,
            road_width=request.road_width,
            distance=request.distance_from_city,
            property_type=request.property_type,
            amenities=request.amenities,
            location=request.location or "Central"
        )
        
        confidence = "high" if result['confidence'] > 95 else "medium" if result['confidence'] > 90 else "low"
        
        return PropertyResponse(
            predicted_price=result['predicted_price'],
            price_per_sqft=result['price_per_sqft'],
            city=request.city,
            area=request.area,
            confidence=confidence
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/stats")
async def get_stats():
    # Mock stats
    city_data = [
        {"city": "mumbai", "avg_price": 18000000, "avg_area": 1200},
        {"city": "delhi", "avg_price": 14000000, "avg_area": 1100},
        {"city": "bangalore", "avg_price": 13000000, "avg_area": 1300},
        {"city": "pune", "avg_price": 9500000, "avg_area": 1250},
        {"city": "hyderabad", "avg_price": 11000000, "avg_area": 1400}
    ]
    
    return {
        "total_records": 100000,
        "cities_covered": 8,
        "overall_avg_price": 13000000,
        "city_stats": city_data
    }

@app.post("/batch_predict")
async def batch_predict(requests: List[PropertyRequest]):
    if not ml_pipeline:
        raise HTTPException(status_code=503, detail="ML pipeline not available")
    
    if len(requests) > 100:
        raise HTTPException(status_code=400, detail="Maximum 100 requests allowed")
    
    results = []
    errors = []
    
    for i, req in enumerate(requests):
        try:
            result = ml_pipeline.predict_price(
                city=req.city,
                area=req.area,
                road_width=req.road_width,
                distance=req.distance_from_city,
                property_type=req.property_type,
                amenities=req.amenities,
                location=req.location or "Central"
            )
            
            results.append({
                "index": i,
                "city": req.city,
                "predicted_price": result['predicted_price'],
                "price_per_sqft": result['price_per_sqft'],
                "confidence": result['confidence']
            })
        except Exception as e:
            errors.append({"index": i, "error": str(e)})
    
    return {
        "predictions": results, 
        "count": len(results),
        "errors": errors,
        "success_rate": len(results) / len(requests) * 100
    }

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}")
    return {"error": "Internal server error", "detail": str(exc)}

if __name__ == "__main__":
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_level="info",
        access_log=True
    )