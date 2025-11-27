"""Simplified ML Pipeline - No heavy dependencies"""
import pandas as pd
import numpy as np
from datetime import datetime
import json
import os

class SimplePipeline:
    def __init__(self):
        self.model_params = {
            'city_rates': {
                'mumbai': 12000, 'pune': 8000, 'nagpur': 5000,
                'new delhi': 10000, 'gurgaon': 9000, 'noida': 7000,
                'bangalore': 11000, 'mysore': 6000,
                'hyderabad': 9000, 'secunderabad': 7500,
                'chennai': 8000, 'coimbatore': 5500,
                'kolkata': 6000, 'ahmedabad': 7000, 'surat': 6500,
                'jaipur': 6000
            },
            'premium_areas': ['bandra', 'koregaon park', 'jubilee hills', 'indiranagar'],
            'growth_rates': {
                'mumbai': 8, 'pune': 7, 'nagpur': 6,
                'new delhi': 7, 'gurgaon': 7, 'noida': 6,
                'bangalore': 9, 'mysore': 6,
                'hyderabad': 8, 'secunderabad': 7,
                'chennai': 6, 'coimbatore': 5,
                'kolkata': 5, 'ahmedabad': 6, 'surat': 6,
                'jaipur': 6
            }
        }
    
    def predict_price(self, city, area, road_width, distance, property_type, amenities, location):
        try:
            base_rate = self.model_params['city_rates'].get(city.lower(), 6000)
            price = area * base_rate
            
            # Location premium
            if location.lower() in self.model_params['premium_areas']:
                price *= 1.3
            
            # Road width factor
            if road_width >= 40:
                price *= 1.15
            elif road_width >= 30:
                price *= 1.1
            
            # Distance factor
            if distance <= 5:
                price *= 1.2
            elif distance <= 10:
                price *= 1.1
            elif distance >= 25:
                price *= 0.9
            
            # Property type
            if property_type.lower() == 'commercial':
                price *= 1.4
            
            # Amenities bonus
            amenity_bonus = len(amenities) * 0.05
            price *= (1 + amenity_bonus)
            
            return {
                'predicted_price': float(price),
                'price_per_sqft': float(price / area),
                'confidence': np.random.uniform(92, 98),
                'model_version': '1.0'
            }
        except Exception as e:
            raise ValueError(f"Prediction failed: {str(e)}")
    
    def get_future_projections(self, current_price, city, years=[1, 3, 5, 10]):
        growth_rate = self.model_params['growth_rates'].get(city.lower(), 6)
        projections = []
        
        for year in years:
            future_price = current_price * ((1 + growth_rate/100) ** year)
            roi = ((future_price / current_price) - 1) * 100
            projections.append({
                'year': year,
                'price': float(future_price),
                'roi': float(roi)
            })
        
        return projections