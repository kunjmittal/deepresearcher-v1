#!/bin/bash

# Set memory optimization
export PYTHONUNBUFFERED=1
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export TOKENIZERS_PARALLELISM=false

# Set port
export PORT=${PORT:-8000}

echo "🚀 Starting Minimal Deep Researcher API..."
echo "📡 Port: $PORT"
echo "💾 Memory optimized for Render free tier"

# Start the minimal API server
python minimal_api.py
