#!/bin/bash

# Download models if they don't exist
echo "🔄 Checking for required models..."
python download_models.py

# Start the application
echo "🚀 Starting Deep Researcher API..."
uvicorn api_server:app --host 0.0.0.0 --port $PORT
