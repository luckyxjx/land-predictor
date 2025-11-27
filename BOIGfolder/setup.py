from setuptools import setup, find_packages

setup(
    name="big-data-land-price",
    version="1.0.0",
    description="Big Data Land Price Analytics Platform",
    author="Your Name",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "pyspark>=3.5.0",
        "pandas>=2.1.0",
        "numpy>=1.24.3",
        "streamlit>=1.28.0",
        "fastapi>=0.104.1",
        "uvicorn>=0.24.0",
        "plotly>=5.17.0",
        "requests>=2.31.0",
        "kafka-python>=2.0.2",
        "redis>=5.0.1",
        "beautifulsoup4>=4.12.2"
    ],
    extras_require={
        "dev": ["pytest", "black", "flake8"],
        "streaming": ["kafka-python", "redis", "websockets"]
    },
    entry_points={
        "console_scripts": [
            "land-price-dashboard=src.ui.big_data_dashboard:main",
            "land-price-api=src.api.api_server:main",
        ],
    },
)