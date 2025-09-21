#!/usr/bin/env python3
"""
Download required models for Deep Researcher Agent.
This script downloads the smallest possible embedding model for Render's free tier.
"""

import os
import sys
from pathlib import Path

def download_embedding_model():
    """Download the smallest embedding model for Render's free tier."""
    # Use the smallest available model
    model_name = "all-MiniLM-L6-v2"
    model_dir = Path("./models/embeddings")
    
    # Create models directory
    model_dir.mkdir(parents=True, exist_ok=True)
    
    # Check if model already exists
    model_path = model_dir / f"models--sentence-transformers--{model_name}"
    if model_path.exists():
        print(f"✅ Model {model_name} already exists at {model_path}")
        return
    
    print(f"🔄 Downloading ultra-lightweight model for Render free tier...")
    print("Using minimal memory footprint...")
    
    try:
        # Set aggressive memory optimization
        os.environ['TOKENIZERS_PARALLELISM'] = 'false'
        os.environ['OMP_NUM_THREADS'] = '1'
        os.environ['MKL_NUM_THREADS'] = '1'
        os.environ['PYTORCH_CUDA_ALLOC_CONF'] = 'max_split_size_mb:128'
        
        # Import only when needed
        from sentence_transformers import SentenceTransformer
        
        print(f"📥 Downloading {model_name} with ultra-aggressive memory optimization...")
        
        # Download with minimal memory
        model = SentenceTransformer(
            model_name,
            device='cpu',
            cache_folder=str(model_dir)
        )
        
        # Get basic info
        embedding_dim = model.get_sentence_embedding_dimension()
        
        # Save minimal metadata
        metadata = {
            "model_name": model_name,
            "embedding_dimension": embedding_dim,
            "device": "cpu",
            "optimized_for": "render_free_tier"
        }
        
        import json
        with open(model_dir / "model_metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
        
        # Aggressive memory cleanup
        print("🧹 Performing ultra-aggressive memory cleanup...")
        del model
        
        # Force multiple garbage collections
        import gc
        for _ in range(5):
            gc.collect()
        
        print(f"✅ Model {model_name} downloaded with ultra-optimization!")
        print(f"📁 Saved to: {model_dir}")
        print("💾 Memory usage minimized for Render free tier")
        
    except Exception as e:
        print(f"❌ Error downloading model: {e}")
        print("🔄 Model will be downloaded on first use with lazy loading")
        
        # Create a minimal metadata file
        metadata = {
            "model_name": model_name,
            "embedding_dimension": 384,
            "device": "cpu",
            "lazy_load": True
        }
        
        import json
        with open(model_dir / "model_metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
        
        print("✅ Lazy loading configuration created")

if __name__ == "__main__":
    download_embedding_model()
