#!/usr/bin/env python3
"""
Big Data Land Price System Launcher
Run different components of the system
"""

import subprocess
import sys
import os
from pathlib import Path

def run_data_generation():
    """Generate big dataset"""
    print("🔄 Generating 100K property records...")
    subprocess.run([sys.executable, "data_generator.py"])
    print("✅ Data generation completed!")

def run_model_training():
    """Train Spark ML model"""
    print("🚀 Training Spark ML model...")
    subprocess.run([sys.executable, "spark_pipeline.py"])
    print("✅ Model training completed!")

def run_ui():
    """Launch Streamlit UI"""
    print("🌐 Launching Big Data UI...")
    subprocess.run(["streamlit", "run", "big_data_ui.py", "--server.port", "8501"])

def run_api():
    """Launch FastAPI server"""
    print("🔌 Starting API server...")
    subprocess.run([sys.executable, "api_server.py"])

def run_full_system():
    """Run complete system setup"""
    print("🏗️ Setting up complete Big Data system...")
    
    # Check if data exists
    if not Path("property_data_large.csv").exists():
        run_data_generation()
    
    # Check if model exists
    if not Path("land_price_model").exists():
        run_model_training()
    
    print("✅ System ready!")
    print("\nAvailable commands:")
    print("- python run_system.py ui      # Launch web interface")
    print("- python run_system.py api     # Start API server")

def show_help():
    """Show available commands"""
    print("""
🏗️ Big Data Land Price System

Commands:
  data      Generate 100K property records
  train     Train Spark ML model  
  ui        Launch Streamlit web interface
  api       Start FastAPI server
  setup     Complete system setup
  help      Show this help

Examples:
  python run_system.py setup
  python run_system.py ui
  python run_system.py api
    """)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    commands = {
        'data': run_data_generation,
        'train': run_model_training,
        'ui': run_ui,
        'api': run_api,
        'setup': run_full_system,
        'help': show_help
    }
    
    if command in commands:
        commands[command]()
    else:
        print(f"❌ Unknown command: {command}")
        show_help()
        sys.exit(1)