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

# Use uvicorn directly for simplicity and reliability
uvicorn api_server:app \
    --host 0.0.0.0 \
    --port $PORT \
    --workers 1 \
    --loop asyncio \
    --http httptools
