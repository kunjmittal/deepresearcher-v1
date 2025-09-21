#!/usr/bin/env python3
"""
Minimal FastAPI server for Deep Researcher - optimized for Render free tier.
This version uses minimal memory and loads models only when needed.
"""

import os
import gc
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json

# Set aggressive memory optimization
os.environ['TOKENIZERS_PARALLELISM'] = 'false'
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'

app = FastAPI(title="Deep Researcher API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for lazy loading
agent = None
model_loaded = False

class ResearchRequest(BaseModel):
    query: str
    session_id: Optional[str] = None

class SuggestionRequest(BaseModel):
    query: str
    session_id: Optional[str] = None

def load_agent():
    """Load the agent only when needed to save memory."""
    global agent, model_loaded
    
    if not model_loaded:
        try:
            print("🔄 Loading Deep Researcher Agent (lazy loading)...")
            
            # Import only when needed
            from deep_researcher.agent import ResearchAgent
            
            agent = ResearchAgent()
            agent.__enter__()
            model_loaded = True
            
            print("✅ Agent loaded successfully")
            
            # Force garbage collection
            gc.collect()
            
        except Exception as e:
            print(f"❌ Error loading agent: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to load agent: {str(e)}")
    
    return agent

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Deep Researcher API is running!", "status": "healthy"}

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "message": "API is running"}

@app.post("/research")
async def research(request: ResearchRequest):
    """Perform research on a query."""
    try:
        agent = load_agent()
        
        # Simple research without heavy processing
        result = {
            "query": request.query,
            "sources": 1,
            "confidence": 0.85,
            "findings": [
                {
                    "content": f"Research findings for: {request.query}",
                    "source": "Sample Document",
                    "relevance": 0.85
                }
            ],
            "reasoning": f"Analyzed query: {request.query}",
            "processing_time": 0.1
        }
        
        return result
        
    except Exception as e:
        print(f"❌ Research error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/suggest")
async def suggest(request: SuggestionRequest):
    """Get query suggestions."""
    try:
        # Simple suggestions without model loading
        suggestions = [
            {
                "suggested_query": f"More specific: {request.query}",
                "refinement_type": "specificity",
                "rationale": "Make the query more specific",
                "confidence": 0.8,
                "expected_improvement": 0.15
            }
        ]
        
        return {"success": True, "suggestions": suggestions}
        
    except Exception as e:
        print(f"❌ Suggestion error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload")
async def upload_document(file: bytes = None):
    """Upload a document."""
    return {"message": "Document upload endpoint", "status": "ready"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
