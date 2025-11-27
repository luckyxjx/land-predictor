from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from spark_pipeline import BigDataPipeline
import uvicorn
from typing import List, Optional

app = FastAPI(title="Big Data Land Price API", version="1.0.0")

# Initialize pipeline
pipeline = BigDataPipeline()

class PropertyRequest(BaseModel):
    city: str
    area: int
    road_width: int
    distance_from_city: int
    property_type: str
    amenities: List[str] = []

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
    try:
        # Test Spark connection
        df = pipeline.load_data('property_data_large.csv')
        record_count = df.count()
        return {
            "status": "healthy",
            "spark_status": "connected",
            "total_records": record_count
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.post("/predict", response_model=PropertyResponse)
async def predict_price(request: PropertyRequest):
    try:
        # Create prediction data
        pred_data = {
            'property_id': 'API_PRED',
            'city': request.city.lower(),
            'area': request.area,
            'road_width': request.road_width,
            'distance_from_city': request.distance_from_city,
            'property_type': request.property_type.lower(),
            'amenities': ','.join(request.amenities),
            'price': 0,
            'timestamp': '2024-01-01T00:00:00',
            'latitude': 12.0,
            'longitude': 77.0
        }
        
        # Load model and predict
        model = pipeline.load_model('land_price_model')
        df_pred = pipeline.spark.createDataFrame([pred_data])
        df_pred = pipeline.feature_engineering(df_pred)
        prediction = model.transform(df_pred)
        price = prediction.select("prediction").collect()[0]["prediction"]
        
        # Determine confidence based on city and features
        confidence = "high" if request.city.lower() in ['mumbai', 'delhi', 'bangalore'] else "medium"
        
        return PropertyResponse(
            predicted_price=float(price),
            price_per_sqft=float(price / request.area),
            city=request.city,
            area=request.area,
            confidence=confidence
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/stats")
async def get_stats():
    try:
        df = pipeline.load_data('property_data_large.csv')
        
        total_records = df.count()
        cities = df.select('city').distinct().count()
        avg_price = df.agg({'price': 'avg'}).collect()[0][0]
        
        # City-wise stats
        city_stats = df.groupBy('city').agg({'price': 'avg', 'area': 'avg'}).collect()
        city_data = [
            {
                "city": row['city'],
                "avg_price": float(row['avg(price)']),
                "avg_area": float(row['avg(area)'])
            }
            for row in city_stats
        ]
        
        return {
            "total_records": total_records,
            "cities_covered": cities,
            "overall_avg_price": float(avg_price),
            "city_stats": city_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stats failed: {str(e)}")

@app.post("/batch_predict")
async def batch_predict(requests: List[PropertyRequest]):
    try:
        results = []
        for req in requests:
            # Individual prediction logic (simplified)
            pred_data = {
                'property_id': f'BATCH_{len(results)}',
                'city': req.city.lower(),
                'area': req.area,
                'road_width': req.road_width,
                'distance_from_city': req.distance_from_city,
                'property_type': req.property_type.lower(),
                'amenities': ','.join(req.amenities),
                'price': 0,
                'timestamp': '2024-01-01T00:00:00',
                'latitude': 12.0,
                'longitude': 77.0
            }
            
            model = pipeline.load_model('land_price_model')
            df_pred = pipeline.spark.createDataFrame([pred_data])
            df_pred = pipeline.feature_engineering(df_pred)
            prediction = model.transform(df_pred)
            price = prediction.select("prediction").collect()[0]["prediction"]
            
            results.append({
                "city": req.city,
                "predicted_price": float(price),
                "price_per_sqft": float(price / req.area)
            })
        
        return {"predictions": results, "count": len(results)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch prediction failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)