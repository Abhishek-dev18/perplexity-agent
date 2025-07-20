from fastapi import FastAPI, HTTPException, Query
from .browser import fetch_perplexity_answer
import logging
import traceback

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Perplexity AI Agent",
    description="Browser automation agent for Perplexity AI searches",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {
        "status": "Perplexity AI Agent is running!",
        "version": "1.0.0",
        "endpoint": "/search?promt=your_question"
    }

@app.get("/search")
def search(promt: str = Query(..., min_length=1, max_length=500, description="Search prompt for Perplexity")):
    try:
        logger.info(f"Processing search request: {promt[:50]}...")
        answer = fetch_perplexity_answer(promt)

        if not answer or len(answer.strip()) < 10:
            logger.warning("Received empty or very short response")
            raise HTTPException(
                status_code=502, 
                detail="No meaningful response received from Perplexity"
            )

        logger.info(f"Search completed successfully, response length: {len(answer)}")
        return {
            "prompt": promt,
            "answer": answer.strip(),
            "status": "success",
            "response_length": len(answer)
        }

    except Exception as e:
        error_msg = str(e)
        logger.error(f"Search failed for prompt '{promt[:50]}...': {error_msg}")
        logger.error(traceback.format_exc())

        raise HTTPException(
            status_code=502, 
            detail=f"Search failed: {error_msg}"
        )

@app.get("/health")
def health_check():
    return {
        "status": "healthy", 
        "service": "perplexity-agent",
        "version": "1.0.0"
    }

@app.get("/test")
def test_endpoint():
    """Simple test endpoint to verify the service is running"""
    try:
        # Test basic functionality without browser automation
        return {
            "status": "test_passed",
            "message": "Service is responding correctly",
            "test_prompt": "Use /search?promt=test to test browser automation"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Test failed: {str(e)}")
