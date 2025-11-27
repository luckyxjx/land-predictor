import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)

class Config:
    """Configuration class for API endpoints and settings"""
    
    # Real Estate APIs
    ACRES_99_API_KEY = os.getenv('ACRES_99_API_KEY', 'demo_key')
    ACRES_99_BASE_URL = os.getenv('ACRES_99_BASE_URL', 'https://api.99acres.com/v1')
    ACRES_99_RATE_LIMIT = int(os.getenv('ACRES_99_RATE_LIMIT', '100'))
    
    MAGICBRICKS_API_KEY = os.getenv('MAGICBRICKS_API_KEY', 'demo_key')
    MAGICBRICKS_BASE_URL = os.getenv('MAGICBRICKS_BASE_URL', 'https://api.magicbricks.com/v2')
    MAGICBRICKS_RATE_LIMIT = int(os.getenv('MAGICBRICKS_RATE_LIMIT', '200'))
    
    HOUSING_API_KEY = os.getenv('HOUSING_API_KEY', 'demo_key')
    HOUSING_BASE_URL = os.getenv('HOUSING_BASE_URL', 'https://api.housing.com/v1')
    HOUSING_RATE_LIMIT = int(os.getenv('HOUSING_RATE_LIMIT', '150'))
    
    # Government APIs
    RERA_API_KEY = os.getenv('RERA_API_KEY', 'demo_key')
    RERA_BASE_URL = os.getenv('RERA_BASE_URL', 'https://rera.gov.in/api/v1')
    
    REGISTRAR_API_KEY = os.getenv('REGISTRAR_API_KEY', 'demo_key')
    REGISTRAR_BASE_URL = os.getenv('REGISTRAR_BASE_URL', 'https://stamps.gov.in/api/v1')
    
    # Market Data APIs
    RBI_API_KEY = os.getenv('RBI_API_KEY', 'demo_key')
    RBI_BASE_URL = os.getenv('RBI_BASE_URL', 'https://api.rbi.org.in/v1')
    
    NSE_API_KEY = os.getenv('NSE_API_KEY', 'demo_key')
    NSE_BASE_URL = os.getenv('NSE_BASE_URL', 'https://api.nseindia.com/v1')
    
    # External APIs
    GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', 'demo_key')
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', 'demo_key')
    NEWS_API_KEY = os.getenv('NEWS_API_KEY', 'demo_key')
    
    # Rate Limiting
    GLOBAL_RATE_LIMIT = int(os.getenv('GLOBAL_RATE_LIMIT', '1000'))
    DAILY_REQUEST_LIMIT = int(os.getenv('DAILY_REQUEST_LIMIT', '5000'))
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', '10'))
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))
    
    # Database
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))
    REDIS_DB = int(os.getenv('REDIS_DB', '0'))
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')
    
    # Kafka
    KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
    KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'property-updates')
    KAFKA_GROUP_ID = os.getenv('KAFKA_GROUP_ID', 'property-consumer-group')
    
    # API Server
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', '8000'))
    API_WORKERS = int(os.getenv('API_WORKERS', '4'))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/api.log')
    
    # Data Validation
    MIN_PRICE = int(os.getenv('MIN_PRICE', '100000'))
    MAX_PRICE = int(os.getenv('MAX_PRICE', '1000000000'))
    MIN_AREA = int(os.getenv('MIN_AREA', '100'))
    MAX_AREA = int(os.getenv('MAX_AREA', '50000'))
    VALID_CITIES = os.getenv('VALID_CITIES', 'mumbai,delhi,bangalore').split(',')
    
    # Security
    API_SECRET_KEY = os.getenv('API_SECRET_KEY', 'default_secret_key')
    JWT_SECRET = os.getenv('JWT_SECRET', 'default_jwt_secret')
    ALLOWED_ORIGINS = os.getenv('ALLOWED_ORIGINS', 'http://localhost:8501').split(',')
    
    @classmethod
    def get_api_config(cls, api_name):
        """Get API configuration for specific service"""
        api_configs = {
            '99acres': {
                'api_key': cls.ACRES_99_API_KEY,
                'base_url': cls.ACRES_99_BASE_URL,
                'rate_limit': cls.ACRES_99_RATE_LIMIT
            },
            'magicbricks': {
                'api_key': cls.MAGICBRICKS_API_KEY,
                'base_url': cls.MAGICBRICKS_BASE_URL,
                'rate_limit': cls.MAGICBRICKS_RATE_LIMIT
            },
            'housing': {
                'api_key': cls.HOUSING_API_KEY,
                'base_url': cls.HOUSING_BASE_URL,
                'rate_limit': cls.HOUSING_RATE_LIMIT
            }
        }
        return api_configs.get(api_name, {})
    
    @classmethod
    def print_config_summary(cls):
        """Print configuration summary"""
        print("🔧 Configuration Summary:")
        print(f"APIs: 99acres, MagicBricks, Housing.com")
        print(f"Rate limit: {cls.GLOBAL_RATE_LIMIT}/day")
        print(f"Redis: {cls.REDIS_HOST}:{cls.REDIS_PORT}")
        print(f"Kafka: {cls.KAFKA_BOOTSTRAP_SERVERS}")

if __name__ == "__main__":
    Config.print_config_summary()