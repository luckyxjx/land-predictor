import pandas as pd
import numpy as np
from datetime import datetime
import re

class PropertyDataValidator:
    def __init__(self):
        self.validation_rules = {
            'price': {'min': 100000, 'max': 1000000000},  # 1L to 100Cr
            'area': {'min': 100, 'max': 50000},           # 100 to 50K sqft
            'road_width': {'min': 5, 'max': 100},         # 5 to 100 ft
            'distance_from_city': {'min': 0, 'max': 100}, # 0 to 100 km
        }
        
        self.valid_cities = [
            'mumbai', 'delhi', 'bangalore', 'hyderabad', 'pune', 
            'chennai', 'kolkata', 'ahmedabad', 'surat', 'jaipur'
        ]
        
        self.valid_property_types = ['residential', 'commercial', 'industrial']
    
    def validate_price(self, price):
        """Validate property price"""
        try:
            price = float(price)
            if self.validation_rules['price']['min'] <= price <= self.validation_rules['price']['max']:
                return True, price
            return False, f"Price {price} out of range"
        except:
            return False, "Invalid price format"
    
    def validate_area(self, area):
        """Validate property area"""
        try:
            area = float(area)
            if self.validation_rules['area']['min'] <= area <= self.validation_rules['area']['max']:
                return True, area
            return False, f"Area {area} out of range"
        except:
            return False, "Invalid area format"
    
    def validate_city(self, city):
        """Validate city name"""
        if isinstance(city, str):
            city_clean = city.lower().strip()
            if city_clean in self.valid_cities:
                return True, city_clean
            return False, f"Unknown city: {city}"
        return False, "Invalid city format"
    
    def validate_property_type(self, prop_type):
        """Validate property type"""
        if isinstance(prop_type, str):
            type_clean = prop_type.lower().strip()
            if type_clean in self.valid_property_types:
                return True, type_clean
            return False, f"Invalid property type: {prop_type}"
        return False, "Invalid property type format"
    
    def validate_coordinates(self, lat, lon):
        """Validate GPS coordinates for India"""
        try:
            lat, lon = float(lat), float(lon)
            # India bounds: Lat 8-37, Lon 68-97
            if 8 <= lat <= 37 and 68 <= lon <= 97:
                return True, (lat, lon)
            return False, "Coordinates outside India"
        except:
            return False, "Invalid coordinate format"
    
    def validate_phone(self, phone):
        """Validate Indian phone number"""
        if isinstance(phone, str):
            # Remove spaces, dashes, +91
            clean_phone = re.sub(r'[\s\-\+]', '', phone)
            clean_phone = clean_phone.replace('91', '', 1) if clean_phone.startswith('91') else clean_phone
            
            # Check if 10 digits starting with 6-9
            if re.match(r'^[6-9]\d{9}$', clean_phone):
                return True, clean_phone
            return False, f"Invalid phone: {phone}"
        return False, "Phone must be string"
    
    def validate_property_record(self, record):
        """Validate complete property record"""
        errors = []
        validated_record = {}
        
        # Required fields validation
        required_fields = ['price', 'area', 'city', 'property_type']
        
        for field in required_fields:
            if field not in record or record[field] is None:
                errors.append(f"Missing required field: {field}")
                continue
            
            # Field-specific validation
            if field == 'price':
                valid, result = self.validate_price(record[field])
            elif field == 'area':
                valid, result = self.validate_area(record[field])
            elif field == 'city':
                valid, result = self.validate_city(record[field])
            elif field == 'property_type':
                valid, result = self.validate_property_type(record[field])
            
            if valid:
                validated_record[field] = result
            else:
                errors.append(f"{field}: {result}")
        
        # Optional fields validation
        if 'latitude' in record and 'longitude' in record:
            valid, result = self.validate_coordinates(record['latitude'], record['longitude'])
            if valid:
                validated_record['latitude'], validated_record['longitude'] = result
            else:
                errors.append(f"Coordinates: {result}")
        
        if 'contact' in record:
            valid, result = self.validate_phone(record['contact'])
            if valid:
                validated_record['contact'] = result
            else:
                errors.append(f"Contact: {result}")
        
        # Price per sqft validation
        if 'price' in validated_record and 'area' in validated_record:
            price_per_sqft = validated_record['price'] / validated_record['area']
            if price_per_sqft < 500 or price_per_sqft > 100000:
                errors.append(f"Unrealistic price per sqft: ₹{price_per_sqft:,.0f}")
        
        # Add validation metadata
        validated_record['validation_status'] = 'valid' if not errors else 'invalid'
        validated_record['validation_errors'] = errors
        validated_record['validated_at'] = datetime.now().isoformat()
        
        return validated_record, errors
    
    def validate_batch(self, data):
        """Validate batch of property records"""
        if isinstance(data, pd.DataFrame):
            records = data.to_dict('records')
        else:
            records = data
        
        validated_records = []
        validation_summary = {
            'total': len(records),
            'valid': 0,
            'invalid': 0,
            'errors': []
        }
        
        for i, record in enumerate(records):
            validated_record, errors = self.validate_property_record(record)
            validated_records.append(validated_record)
            
            if errors:
                validation_summary['invalid'] += 1
                validation_summary['errors'].extend([f"Record {i}: {error}" for error in errors])
            else:
                validation_summary['valid'] += 1
        
        return validated_records, validation_summary
    
    def clean_and_standardize(self, record):
        """Clean and standardize property data"""
        cleaned = {}
        
        # Standardize city names
        if 'city' in record:
            city_mapping = {
                'new delhi': 'delhi',
                'navi mumbai': 'mumbai',
                'greater noida': 'noida',
                'bengaluru': 'bangalore'
            }
            city = record['city'].lower().strip()
            cleaned['city'] = city_mapping.get(city, city)
        
        # Standardize property types
        if 'property_type' in record:
            type_mapping = {
                'apartment': 'residential',
                'villa': 'residential',
                'house': 'residential',
                'office': 'commercial',
                'shop': 'commercial',
                'warehouse': 'industrial'
            }
            prop_type = record['property_type'].lower().strip()
            cleaned['property_type'] = type_mapping.get(prop_type, prop_type)
        
        # Copy other fields
        for key, value in record.items():
            if key not in cleaned:
                cleaned[key] = value
        
        return cleaned

if __name__ == "__main__":
    validator = PropertyDataValidator()
    
    # Test with sample data
    test_record = {
        'price': 5000000,
        'area': 1200,
        'city': 'Mumbai',
        'property_type': 'Residential',
        'latitude': 19.0760,
        'longitude': 72.8777,
        'contact': '+91-9876543210'
    }
    
    validated, errors = validator.validate_property_record(test_record)
    
    if errors:
        print("❌ Validation errors:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("✅ Record is valid!")
        print(f"Validated record: {validated}")