from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, split, size, regexp_replace, to_timestamp
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, TimestampType
from pyspark.ml.feature import VectorAssembler, StringIndexer, StandardScaler
from pyspark.ml.regression import RandomForestRegressor, GBTRegressor
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml import Pipeline
import os

class BigDataPipeline:
    def __init__(self):
        self.spark = SparkSession.builder \
            .appName("LandPriceBigData") \
            .config("spark.sql.adaptive.enabled", "true") \
            .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
            .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
            .getOrCreate()
        
        self.spark.sparkContext.setLogLevel("WARN")
    
    def load_data(self, file_path):
        """Load data with optimized settings"""
        df = self.spark.read.csv(file_path, header=True, inferSchema=True)
        print(f"Loaded {df.count()} records")
        return df
    
    def feature_engineering(self, df):
        """Advanced feature engineering at scale"""
        # Parse amenities count
        df = df.withColumn('amenity_count', 
                          when(col('amenities').isNull(), 0)
                          .otherwise(size(split(col('amenities'), ','))))
        
        # Price per sqft
        df = df.withColumn('price_per_sqft', col('price') / col('area'))
        
        # Distance categories
        df = df.withColumn('distance_category',
                          when(col('distance_from_city') <= 5, 'very_close')
                          .when(col('distance_from_city') <= 15, 'close')
                          .when(col('distance_from_city') <= 30, 'moderate')
                          .otherwise('far'))
        
        # Road width categories
        df = df.withColumn('road_category',
                          when(col('road_width') >= 40, 'wide')
                          .when(col('road_width') >= 25, 'medium')
                          .otherwise('narrow'))
        
        # Time-based features if timestamp exists
        if 'timestamp' in df.columns:
            df = df.withColumn('timestamp', to_timestamp(col('timestamp')))
            df = df.withColumn('year', col('timestamp').substr(1, 4).cast('int'))
            df = df.withColumn('month', col('timestamp').substr(6, 2).cast('int'))
        
        return df
    
    def build_ml_pipeline(self):
        """Build scalable ML pipeline"""
        # String indexers for categorical variables
        city_indexer = StringIndexer(inputCol="city", outputCol="city_indexed", handleInvalid="keep")
        type_indexer = StringIndexer(inputCol="property_type", outputCol="type_indexed", handleInvalid="keep")
        distance_indexer = StringIndexer(inputCol="distance_category", outputCol="distance_cat_indexed", handleInvalid="keep")
        road_indexer = StringIndexer(inputCol="road_category", outputCol="road_cat_indexed", handleInvalid="keep")
        
        # Feature assembler
        feature_cols = ['area', 'road_width', 'distance_from_city', 'amenity_count',
                       'city_indexed', 'type_indexed', 'distance_cat_indexed', 'road_cat_indexed']
        
        assembler = VectorAssembler(inputCols=feature_cols, outputCol="features_raw")
        
        # Feature scaling
        scaler = StandardScaler(inputCol="features_raw", outputCol="features")
        
        # Model - using GBT for better performance
        gbt = GBTRegressor(featuresCol="features", labelCol="price", 
                          maxIter=100, maxDepth=8, stepSize=0.1)
        
        # Create pipeline
        pipeline = Pipeline(stages=[
            city_indexer, type_indexer, distance_indexer, road_indexer,
            assembler, scaler, gbt
        ])
        
        return pipeline
    
    def train_model(self, df):
        """Train model on large dataset"""
        # Feature engineering
        df = self.feature_engineering(df)
        
        # Split data
        train_df, test_df = df.randomSplit([0.8, 0.2], seed=42)
        
        print(f"Training on {train_df.count()} records")
        print(f"Testing on {test_df.count()} records")
        
        # Build and train pipeline
        pipeline = self.build_ml_pipeline()
        model = pipeline.fit(train_df)
        
        # Evaluate
        predictions = model.transform(test_df)
        evaluator = RegressionEvaluator(labelCol="price", predictionCol="prediction")
        
        mae = evaluator.evaluate(predictions, {evaluator.metricName: "mae"})
        rmse = evaluator.evaluate(predictions, {evaluator.metricName: "rmse"})
        r2 = evaluator.evaluate(predictions, {evaluator.metricName: "r2"})
        
        print(f"Model Performance:")
        print(f"MAE: ₹{mae:,.0f}")
        print(f"RMSE: ₹{rmse:,.0f}")
        print(f"R²: {r2:.3f}")
        
        return model, (mae, rmse, r2)
    
    def batch_predict(self, model, df):
        """Batch predictions for large datasets"""
        df = self.feature_engineering(df)
        predictions = model.transform(df)
        return predictions.select("property_id", "city", "area", "price", "prediction")
    
    def save_model(self, model, path):
        """Save trained model"""
        model.write().overwrite().save(path)
        print(f"Model saved to {path}")
    
    def load_model(self, path):
        """Load saved model"""
        from pyspark.ml import PipelineModel
        return PipelineModel.load(path)

if __name__ == "__main__":
    pipeline = BigDataPipeline()
    
    # Load existing data
    df = pipeline.load_data('property_data_large.csv')
    
    # Train model
    model, metrics = pipeline.train_model(df)
    
    # Save model
    pipeline.save_model(model, 'land_price_model')
    
    print("Big Data pipeline completed!")