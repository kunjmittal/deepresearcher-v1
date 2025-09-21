#!/bin/bash

# Set memory optimization
export PYTHONUNBUFFERED=1
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1

# Download models if they don't exist
echo "🔄 Checking for required models..."
python download_models.py

# Clear any cached models to free memory
echo "🧹 Clearing model cache to free memory..."
python -c "import gc; gc.collect()"

# Start the application with memory optimization
echo "🚀 Starting Deep Researcher API with memory optimization..."
uvicorn api_server:app --host 0.0.0.0 --port $PORT --workers 1
