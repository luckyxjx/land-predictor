import requests
from bs4 import BeautifulSoup
import json
import time
import random
from datetime import datetime
import pandas as pd

class PropertyScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def scrape_99acres_sample(self, city='mumbai', pages=2):
        """Simulate 99acres scraping (demo data)"""
        print(f"🕷️ Scraping {city} properties...")
        
        properties = []
        for page in range(1, pages + 1):
            # Simulate API-like response
            sample_data = self._generate_sample_listings(city, page)
            properties.extend(sample_data)
            time.sleep(random.uniform(1, 3))  # Respectful scraping
        
        return properties
    
    def _generate_sample_listings(self, city, page):
        """Generate realistic property listings"""
        listings = []
        
        for i in range(10):  # 10 properties per page
            property_id = f"{city.upper()}_{page}_{i:03d}"
            
            # City-specific pricing
            base_prices = {
                'mumbai': (8000, 25000),
                'delhi': (6000, 20000),
                'bangalore': (5000, 18000),
                'pune': (4000, 15000),
                'hyderabad': (3500, 12000)
            }
            
            min_price, max_price = base_prices.get(city, (3000, 10000))
            price_per_sqft = random.randint(min_price, max_price)
            area = random.randint(600, 3000)
            
            listing = {
                'property_id': property_id,
                'title': f"{random.choice(['2BHK', '3BHK', '4BHK'])} Apartment in {city.title()}",
                'city': city,
                'area': area,
                'price': area * price_per_sqft,
                'price_per_sqft': price_per_sqft,
                'property_type': random.choice(['residential', 'commercial']),
                'bedrooms': random.choice([1, 2, 3, 4]),
                'bathrooms': random.choice([1, 2, 3]),
                'amenities': random.sample(['gym', 'pool', 'parking', 'security', 'garden'], 
                                         random.randint(2, 4)),
                'locality': f"{city.title()} Sector {random.randint(1, 50)}",
                'posted_date': datetime.now().isoformat(),
                'source': '99acres',
                'url': f"https://99acres.com/property/{property_id}"
            }
            listings.append(listing)
        
        return listings
    
    def scrape_magicbricks_sample(self, city='delhi', pages=2):
        """Simulate MagicBricks scraping"""
        print(f"🏗️ Scraping MagicBricks {city}...")
        
        properties = []
        for page in range(1, pages + 1):
            sample_data = self._generate_magicbricks_listings(city, page)
            properties.extend(sample_data)
            time.sleep(random.uniform(1, 2))
        
        return properties
    
    def _generate_magicbricks_listings(self, city, page):
        """Generate MagicBricks-style listings"""
        listings = []
        
        for i in range(8):  # 8 properties per page
            property_id = f"MB_{city.upper()}_{page}_{i:03d}"
            
            listing = {
                'property_id': property_id,
                'title': f"Premium {random.choice(['Villa', 'Apartment', 'Plot'])} in {city.title()}",
                'city': city,
                'area': random.randint(800, 4000),
                'price': random.randint(2000000, 15000000),
                'property_type': random.choice(['residential', 'commercial', 'industrial']),
                'floor': random.randint(1, 20),
                'total_floors': random.randint(5, 25),
                'age': random.choice(['Under Construction', '1-5 years', '5-10 years', '10+ years']),
                'furnishing': random.choice(['Furnished', 'Semi-Furnished', 'Unfurnished']),
                'parking': random.choice([0, 1, 2, 3]),
                'locality': f"{city.title()} Zone {random.randint(1, 10)}",
                'posted_date': datetime.now().isoformat(),
                'source': 'magicbricks',
                'contact': f"+91-{random.randint(7000000000, 9999999999)}"
            }
            listings.append(listing)
        
        return listings
    
    def get_government_data_sample(self, state='maharashtra'):
        """Simulate government registry data"""
        print(f"🏛️ Fetching {state} registry data...")
        
        # Simulate RERA/registrar data
        registry_data = []
        for i in range(20):
            record = {
                'registration_id': f"REG_{state.upper()}_{i:05d}",
                'state': state,
                'district': random.choice(['Mumbai', 'Pune', 'Nagpur', 'Nashik']),
                'property_type': random.choice(['residential', 'commercial', 'agricultural']),
                'area_sqft': random.randint(500, 5000),
                'sale_price': random.randint(1000000, 20000000),
                'registration_date': datetime.now().isoformat(),
                'buyer_type': random.choice(['individual', 'company', 'trust']),
                'seller_type': random.choice(['individual', 'builder', 'company']),
                'stamp_duty': random.randint(50000, 500000),
                'registration_fee': random.randint(10000, 100000),
                'source': 'government_registry'
            }
            registry_data.append(record)
        
        return registry_data
    
    def scrape_all_sources(self, cities=['mumbai', 'delhi', 'bangalore']):
        """Scrape from multiple sources"""
        all_data = []
        
        for city in cities:
            # 99acres data
            acres_data = self.scrape_99acres_sample(city, pages=2)
            all_data.extend(acres_data)
            
            # MagicBricks data
            mb_data = self.scrape_magicbricks_sample(city, pages=2)
            all_data.extend(mb_data)
        
        # Government data
        gov_data = self.get_government_data_sample()
        all_data.extend(gov_data)
        
        return all_data
    
    def save_scraped_data(self, data, filename='scraped_properties.json'):
        """Save scraped data to file"""
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"💾 Saved {len(data)} properties to {filename}")
        
        # Also save as CSV for analysis
        df = pd.DataFrame(data)
        csv_filename = filename.replace('.json', '.csv')
        df.to_csv(csv_filename, index=False)
        print(f"💾 Saved CSV to {csv_filename}")

if __name__ == "__main__":
    scraper = PropertyScraper()
    
    # Scrape from all sources
    all_properties = scraper.scrape_all_sources(['mumbai', 'delhi', 'bangalore'])
    
    # Save data
    scraper.save_scraped_data(all_properties)
    
    print(f"✅ Scraping completed! Total properties: {len(all_properties)}")