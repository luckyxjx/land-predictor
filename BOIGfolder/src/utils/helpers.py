"""Utility functions for the application"""
import os
import logging
from typing import Dict, Any

def format_indian_currency(amount: float) -> str:
    """Format amount in Indian currency format"""
    if amount >= 10000000:
        return f"₹{amount/10000000:.1f} Cr"
    elif amount >= 100000:
        return f"₹{amount/100000:.1f} L"
    elif amount >= 1000:
        return f"₹{amount/1000:.0f}K"
    else:
        return f"₹{amount:,.0f}"

def validate_input(data: Dict[str, Any]) -> Dict[str, str]:
    """Validate input data and return errors if any"""
    errors = {}
    
    if not data.get('city'):
        errors['city'] = 'City is required'
    
    area = data.get('area', 0)
    if not isinstance(area, (int, float)) or area < 100 or area > 50000:
        errors['area'] = 'Area must be between 100 and 50000 sq ft'
    
    return errors

def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """Setup application logging"""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def ensure_directories():
    """Ensure required directories exist"""
    dirs = ['data/raw', 'data/processed', 'data/models', 'logs']
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)