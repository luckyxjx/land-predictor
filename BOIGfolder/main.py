#!/usr/bin/env python3
"""
Big Data Land Price Analytics Platform
Production Entry Point
"""
import sys
import os
import logging
import socket
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add src to Python path
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

def find_free_port(start_port):
    """Find next available port"""
    for port in range(start_port, start_port + 10):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('localhost', port)) != 0:
                return port
    return None

def run_dashboard():
    """Run the Streamlit dashboard"""
    try:
        port = find_free_port(8501)
        if not port:
            logger.error("No available ports found")
            sys.exit(1)
        
        logger.info(f"Starting dashboard on port {port}...")
        os.system(f"streamlit run simple_app.py --server.port {port}")
    except Exception as e:
        logger.error(f"Failed to start dashboard: {e}")
        sys.exit(1)

def run_api():
    """Run the FastAPI server"""
    try:
        port = find_free_port(8000)
        if not port:
            logger.error("No available ports found")
            sys.exit(1)
            
        logger.info(f"Starting API server on port {port}...")
        from api.api_server import app
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
    except Exception as e:
        logger.error(f"Failed to start API: {e}")
        sys.exit(1)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Big Data Land Price Analytics")
    parser.add_argument("--mode", choices=["dashboard", "api"], default="dashboard",
                       help="Run mode: dashboard or api")
    
    args = parser.parse_args()
    
    if args.mode == "dashboard":
        run_dashboard()
    elif args.mode == "api":
        run_api()