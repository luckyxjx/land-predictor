import requests
import time
import json
from datetime import datetime
import random
from data_validator import PropertyDataValidator

class RealEstateAPIClient:
    def __init__(self):
        self.validator = PropertyDataValidator()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 1  # 1 second between requests
        self.daily_request_count = 0
        self.daily_limit = 1000
        
        # API endpoints (demo URLs - replace with real ones)
        self.apis = {
            '99acres': {
                'base_url': 'https://api.99acres.com/v1',
                'endpoints': {
                    'search': '/properties/search',
                    'details': '/properties/{id}'
                },
                'api_key': 'your_99acres_key',
                'rate_limit': 100  # requests per hour
            },
            'magicbricks': {
                'base_url': 'https://api.magicbricks.com/v2',
                'endpoints': {
                    'listings': '/listings',
                    'property': '/property/{id}'
                },
                'api_key': 'your_magicbricks_key',
                'rate_limit': 200
            }
        }
    
    def rate_limit_check(self):
        """Enforce rate limiting"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            print(f"⏳ Rate limiting: sleeping {sleep_time:.2f}s")
            time.sleep(sleep_time)
        
        if self.daily_request_count >= self.daily_limit:
            raise Exception(f"Daily API limit reached: {self.daily_limit}")
        
        self.last_request_time = time.time()
        self.daily_request_count += 1
    
    def make_api_request(self, url, params=None, retries=3):
        """Make API request with error handling and retries"""
        self.rate_limit_check()
        
        for attempt in range(retries):
            try:
                response = self.session.get(url, params=params, timeout=10)
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 429:  # Rate limited
                    wait_time = 2 ** attempt  # Exponential backoff
                    print(f"⚠️ Rate limited, waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                elif response.status_code == 403:
                    raise Exception("API access forbidden - check API key")
                else:
                    print(f"❌ API error {response.status_code}: {response.text}")
                    
            except requests.exceptions.Timeout:
                print(f"⏰ Request timeout, attempt {attempt + 1}/{retries}")
            except requests.exceptions.ConnectionError:
                print(f"🔌 Connection error, attempt {attempt + 1}/{retries}")
            except Exception as e:
                print(f"❌ Request failed: {e}")
            
            if attempt < retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
        
        return None
    
    def fetch_99acres_properties(self, city, limit=10):
        """Fetch properties from 99acres API (simulated)"""
        print(f"🏠 Fetching {limit} properties from 99acres for {city}...")
        
        # Simulate API response (replace with real API call)
        properties = []
        for i in range(limit):
            # This would be: response = self.make_api_request(api_url, params)
            property_data = self._simulate_99acres_response(city, i)
            
            # Validate data
            try:
                validated_data, errors = self.validator.validate_property_record(property_data)
                
                if not errors:
                    properties.append(validated_data)
                    print(f"✅ Valid property: {validated_data.get('property_id', 'Unknown')}")
                else:
                    print(f"❌ Invalid property: {errors}")
            except Exception as e:
                print(f"❌ Validation error: {e}")
        
        return properties
    
    def fetch_magicbricks_properties(self, city, limit=10):
        """Fetch properties from MagicBricks API (simulated)"""
        print(f"🏗️ Fetching {limit} properties from MagicBricks for {city}...")
        
        properties = []
        for i in range(limit):
            property_data = self._simulate_magicbricks_response(city, i)
            
            # Clean and standardize
            cleaned_data = self.validator.clean_and_standardize(property_data)
            
            # Validate
            try:
                validated_data, errors = self.validator.validate_property_record(cleaned_data)
                
                if not errors:
                    properties.append(validated_data)
                    print(f"✅ Valid property: {validated_data.get('property_id', 'Unknown')}")
                else:
                    print(f"❌ Invalid property: {errors}")
            except Exception as e:
                print(f"❌ Validation error: {e}")
        
        return properties
    
    def _simulate_99acres_response(self, city, index):
        """Simulate 99acres API response"""
        base_prices = {
            'mumbai': 15000, 'delhi': 12000, 'bangalore': 11000,
            'pune': 8000, 'hyderabad': 9000, 'chennai': 8000
        }
        
        base_rate = base_prices.get(city, 6000)
        area = random.randint(600, 3000)
        
        return {
            'property_id': f'99A_{city.upper()}_{index:04d}',
            'title': f'{random.choice(["2BHK", "3BHK", "4BHK"])} Apartment',
            'price': area * base_rate * random.uniform(0.8, 1.2),
            'area': area,
            'city': city,
            'property_type': 'residential',
            'bedrooms': random.choice([2, 3, 4]),
            'bathrooms': random.choice([1, 2, 3]),
            'latitude': 19.0760 + random.uniform(-0.5, 0.5),
            'longitude': 72.8777 + random.uniform(-0.5, 0.5),
            'contact': f'9{random.randint(100000000, 999999999)}',
            'posted_date': datetime.now().isoformat(),
            'source': '99acres'
        }
    
    def _simulate_magicbricks_response(self, city, index):
        """Simulate MagicBricks API response"""
        return {
            'property_id': f'MB_{city.upper()}_{index:04d}',
            'title': f'Premium {random.choice(["Villa", "Apartment"])}',
            'price': random.randint(2000000, 15000000),
            'area': random.randint(800, 4000),
            'city': city.title(),  # Different case to test standardization
            'property_type': random.choice(['Apartment', 'Villa', 'Office']),
            'floor': random.randint(1, 20),
            'total_floors': random.randint(5, 25),
            'furnishing': random.choice(['Furnished', 'Semi-Furnished', 'Unfurnished']),
            'latitude': 19.0760 + random.uniform(-0.5, 0.5),
            'longitude': 72.8777 + random.uniform(-0.5, 0.5),
            'contact': f'+91-9{random.randint(100000000, 999999999)}',
            'source': 'magicbricks'
        }
    
    def fetch_all_sources(self, city, limit_per_source=5):
        """Fetch from all available sources"""
        all_properties = []
        
        try:
            # 99acres
            properties_99 = self.fetch_99acres_properties(city, limit_per_source)
            all_properties.extend(properties_99)
            
            # MagicBricks
            properties_mb = self.fetch_magicbricks_properties(city, limit_per_source)
            all_properties.extend(properties_mb)
            
        except Exception as e:
            print(f"❌ Error fetching data: {e}")
        
        # Validation summary
        valid_count = len([p for p in all_properties if p['validation_status'] == 'valid'])
        
        print(f"\n📊 Fetch Summary:")
        print(f"Total properties: {len(all_properties)}")
        print(f"Valid properties: {valid_count}")
        print(f"API requests made: {self.daily_request_count}")
        
        return all_properties
    
    def save_validated_data(self, properties, filename=None):
        """Save validated data to file"""
        if not filename:
            filename = f"validated_properties_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(properties, f, indent=2)
        
        print(f"💾 Saved {len(properties)} properties to {filename}")

if __name__ == "__main__":
    client = RealEstateAPIClient()
    
    # Test with multiple cities
    cities = ['mumbai', 'delhi', 'bangalore']
    
    for city in cities:
        print(f"\n🏙️ Processing {city.title()}...")
        properties = client.fetch_all_sources(city, limit_per_source=3)
        
        if properties:
            client.save_validated_data(properties, f"{city}_properties.json")
        
        # Rate limiting between cities
        time.sleep(2)