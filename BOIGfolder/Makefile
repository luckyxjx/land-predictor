# Big Data Land Price Analytics Platform

.PHONY: install setup data train ui api dashboard streaming clean test

# Installation
install:
	pip install -r config/requirements.txt
	pip install -r config/streaming_requirements.txt

setup: install
	python scripts/run_system.py setup

# Data operations
data:
	python src/data/data_generator.py

scrape:
	python src/data/web_scraper.py

# ML operations
train:
	python src/ml/spark_pipeline.py

# UI operations
ui:
	streamlit run src/ui/big_data_ui.py --server.port 8502

dashboard:
	streamlit run src/ui/big_data_dashboard.py --server.port 8504

realtime:
	streamlit run src/ui/realtime_ui.py --server.port 8503

# API operations
api:
	python src/api/api_server.py

# Streaming operations
producer:
	python src/streaming/free_data_producer.py

producer-validated:
	python src/streaming/validated_kafka_producer.py

producer-old:
	python src/streaming/kafka_producer_fixed.py

consumer:
	python src/streaming/kafka_consumer_fixed.py

# Data validation
validate:
	python src/data/data_validator.py

api-test:
	python src/data/real_estate_api.py

# Configuration
config:
	python src/config/env_config.py

setup-env:
	cp .env.example .env
	@echo "✅ Created .env file. Edit it with your API keys."

streaming: producer consumer

# Development
test:
	pytest tests/

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf logs/*.log

# Quick start
start: dashboard

# Full system
full: data train dashboard api