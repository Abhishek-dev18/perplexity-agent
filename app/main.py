from fastapi import FastAPI, HTTPException, Query
from .browser import fetch_perplexity_answer
import logging

app = FastAPI(title="Perplexity AI Agent", version="2.0")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/")
def read_root():
    return {
        "status": "Perplexity AI Agent is running",
        "version": "2.0 - Direct URL Approach",
        "message": "Use GET /search?prompt=your_question to query Perplexity AI"
    }

@app.get("/search")
def search(prompt: str = Query(..., min_length=1, max_length=500, alias="promt")):
    """
    Search endpoint that accepts both 'prompt' and 'promt' parameters
    for backward compatibility with existing implementations
    """
    try:
        logger.info(f"Processing search request: {prompt[:100]}...")
        
        # Use the new direct URL approach
        answer = fetch_perplexity_answer(prompt)
        
        if not answer or len(answer.strip()) < 10:
            raise HTTPException(
                status_code=502, 
                detail="No meaningful response received from Perplexity"
            )
            
        logger.info(f"Successfully retrieved answer of length: {len(answer)}")
        
        return {
            "prompt": prompt,
            "answer": answer.strip(),
            "status": "success",
            "method": "direct_url",
            "timestamp": "2025-07-21"
        }
        
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Search failed: {error_msg}")
        
        # Provide helpful error messages
        if "Could not extract meaningful content" in error_msg:
            raise HTTPException(
                status_code=502,
                detail="Perplexity page loaded but no answer content was found. Try rephrasing your query."
            )
        elif "timeout" in error_msg.lower():
            raise HTTPException(
                status_code=504,
                detail="Request timed out. Perplexity may be taking longer than expected to respond."
            )
        else:
            raise HTTPException(
                status_code=502, 
                detail=f"Search failed: {error_msg}"
            )

@app.get("/health")
def health_check():
    return {
        "status": "healthy", 
        "service": "perplexity-agent",
        "approach": "direct-url"
    }

@app.get("/test")
def test_search():
    """
    Quick test endpoint to verify the service is working
    """
    try:
        test_prompt = "What is artificial intelligence?"
        result = fetch_perplexity_answer(test_prompt)
        return {
            "test": "success",
            "prompt": test_prompt,
            "response_length": len(result),
            "preview": result[:200] + "..." if len(result) > 200 else result
        }
    except Exception as e:
        return {
            "test": "failed",
            "error": str(e)
        }
