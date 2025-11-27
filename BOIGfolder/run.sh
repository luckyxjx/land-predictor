#!/bin/bash
# Production deployment script for Big Data Land Price Analytics

set -e  # Exit on any error

echo "🏗️ Starting Big Data Land Price Analytics Platform..."

# Check Python version
if ! python3 --version | grep -q "Python 3.[8-9]\|Python 3.1[0-9]"; then
    echo "Error: Python 3.8+ required"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if data directory exists
if [ ! -d "data" ]; then
    echo "Creating data directory..."
    mkdir -p data/raw data/processed
fi

# Check for running processes on common ports
echo "Checking for port conflicts..."
if lsof -Pi :8501 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  Port 8501 in use, will find alternative"
fi

if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  Port 8000 in use, will find alternative"
fi

# Run based on argument
MODE=${1:-dashboard}

if [ "$MODE" = "api" ]; then
    echo "🚀 Launching API server..."
    python main.py --mode api
else
    echo "🚀 Launching dashboard..."
    python main.py --mode dashboard
fi