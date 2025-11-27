import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import random

class BigDataGenerator:
    def __init__(self):
        self.cities = {
            'mumbai': {'base_rate': 15000, 'growth': 0.08},
            'delhi': {'base_rate': 12000, 'growth': 0.07},
            'bangalore': {'base_rate': 11000, 'growth': 0.09},
            'hyderabad': {'base_rate': 9000, 'growth': 0.08},
            'pune': {'base_rate': 8000, 'growth': 0.07},
            'chennai': {'base_rate': 8000, 'growth': 0.06},
            'kolkata': {'base_rate': 6000, 'growth': 0.05},
            'ahmedabad': {'base_rate': 7000, 'growth': 0.06}
        }
        
        self.amenities = ['school', 'hospital', 'mall', 'park', 'metro', 'airport', 'it_hub']
        self.property_types = ['residential', 'commercial', 'industrial']
    
    def generate_batch_data(self, num_records=100000):
        """Generate large batch of property data"""
        data = []
        
        for i in range(num_records):
            city = random.choice(list(self.cities.keys()))
            city_info = self.cities[city]
            
            # Generate property features
            area = np.random.randint(500, 5000)
            road_width = random.choice([15, 20, 25, 30, 40, 50])
            distance = np.random.randint(1, 50)
            property_type = random.choice(self.property_types)
            
            # Random amenities
            num_amenities = np.random.randint(0, 5)
            selected_amenities = random.sample(self.amenities, num_amenities)
            
            # Calculate price with realistic factors
            base_price = area * city_info['base_rate']
            
            # Apply multipliers
            if road_width >= 40: base_price *= 1.15
            elif road_width >= 30: base_price *= 1.1
            
            if distance <= 5: base_price *= 1.3
            elif distance <= 10: base_price *= 1.15
            elif distance >= 30: base_price *= 0.8
            
            if property_type == 'commercial': base_price *= 1.5
            elif property_type == 'industrial': base_price *= 0.8
            
            # Amenity bonus
            base_price *= (1 + len(selected_amenities) * 0.05)
            
            # Add some noise
            base_price *= np.random.uniform(0.9, 1.1)
            
            # Generate timestamp (last 2 years)
            days_ago = np.random.randint(0, 730)
            timestamp = datetime.now() - timedelta(days=days_ago)
            
            data.append({
                'property_id': f'PROP_{i:06d}',
                'city': city,
                'area': area,
                'road_width': road_width,
                'distance_from_city': distance,
                'property_type': property_type,
                'amenities': ','.join(selected_amenities),
                'price': int(base_price),
                'timestamp': timestamp.isoformat(),
                'latitude': np.random.uniform(12.0, 28.0),
                'longitude': np.random.uniform(72.0, 88.0)
            })
        
        return pd.DataFrame(data)
    
    def generate_streaming_data(self):
        """Generate single record for streaming"""
        return self.generate_batch_data(1).iloc[0].to_dict()

if __name__ == "__main__":
    generator = BigDataGenerator()
    
    # Generate large dataset
    print("Generating 100K property records...")
    df = generator.generate_batch_data(100000)
    
    # Save as CSV for compatibility
    df.to_csv('property_data_large.csv', index=False)
    print(f"Generated {len(df)} records")
    print(f"Data size: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    print(f"Cities: {df['city'].nunique()}")
    print(f"Price range: ₹{df['price'].min():,} - ₹{df['price'].max():,}")
    print("Saved as property_data_large.csv")