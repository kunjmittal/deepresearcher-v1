#!/bin/bash

# Set aggressive memory optimization
export PYTHONUNBUFFERED=1
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export TOKENIZERS_PARALLELISM=false
export PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:128

# Set port explicitly
export PORT=${PORT:-10000}

echo "🔧 Memory optimization settings applied"
echo "📡 Using port: $PORT"

# Skip model download to save memory - use lazy loading
echo "🔄 Skipping model download - using lazy loading to save memory..."

# Start the application with ultra-minimal memory usage
echo "🚀 Starting Deep Researcher API with ultra-minimal memory usage..."
echo "📡 Server will be available on port $PORT"

# Use gunicorn for better memory management
gunicorn api_server:app \
    --bind 0.0.0.0:$PORT \
    --workers 1 \
    --worker-class uvicorn.workers.UvicornWorker \
    --worker-connections 1 \
    --max-requests 100 \
    --max-requests-jitter 10 \
    --timeout 30 \
    --keep-alive 2 \
    --preload-app
