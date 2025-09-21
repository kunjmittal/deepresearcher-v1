#!/usr/bin/env python3
"""
Download required models for Deep Researcher Agent.
This script downloads a lightweight embedding model optimized for Render's free tier.
"""

import os
import sys
from pathlib import Path

def download_embedding_model():
    """Download a lightweight embedding model for Render's free tier."""
    model_name = "all-MiniLM-L6-v2"
    model_dir = Path("./models/embeddings")
    
    # Create models directory
    model_dir.mkdir(parents=True, exist_ok=True)
    
    # Check if model already exists
    model_path = model_dir / f"models--sentence-transformers--{model_name}"
    if model_path.exists():
        print(f"✅ Model {model_name} already exists at {model_path}")
        return
    
    print(f"🔄 Setting up lightweight model for Render free tier...")
    print("Using model caching to reduce memory usage...")
    
    try:
        # Import only when needed to save memory
        from sentence_transformers import SentenceTransformer
        
        # Download with memory optimization
        print(f"📥 Downloading {model_name} with memory optimization...")
        
        # Use a smaller model for free tier
        model = SentenceTransformer(model_name, device='cpu')
        
        # Save to custom location
        model.save(str(model_dir / f"models--sentence-transformers--{model_name}"))
        
        # Clear memory
        del model
        
        print(f"✅ Model {model_name} downloaded successfully!")
        print(f"📁 Saved to: {model_dir}")
        
    except Exception as e:
        print(f"❌ Error downloading model: {e}")
        print("The model will be downloaded automatically on first use.")
        return

if __name__ == "__main__":
    download_embedding_model()
