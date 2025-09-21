#!/usr/bin/env python3
"""
Download required models for Deep Researcher Agent.
This script downloads the embedding model on first run.
"""

import os
import sys
from pathlib import Path
from sentence_transformers import SentenceTransformer

def download_embedding_model():
    """Download the embedding model if it doesn't exist."""
    model_name = "all-MiniLM-L6-v2"
    model_dir = Path("./models/embeddings")
    
    # Create models directory
    model_dir.mkdir(parents=True, exist_ok=True)
    
    # Check if model already exists
    model_path = model_dir / f"models--sentence-transformers--{model_name}"
    if model_path.exists():
        print(f"✅ Model {model_name} already exists at {model_path}")
        return
    
    print(f"🔄 Downloading embedding model: {model_name}")
    print("This may take a few minutes...")
    
    try:
        # Download the model
        model = SentenceTransformer(model_name)
        
        # Save to custom location
        model.save(str(model_dir / f"models--sentence-transformers--{model_name}"))
        
        print(f"✅ Model {model_name} downloaded successfully!")
        print(f"📁 Saved to: {model_dir}")
        
    except Exception as e:
        print(f"❌ Error downloading model: {e}")
        print("The model will be downloaded automatically on first use.")
        return

if __name__ == "__main__":
    download_embedding_model()
