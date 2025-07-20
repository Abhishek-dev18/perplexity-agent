from fastapi import FastAPI, HTTPException, Query
from .browser import fetch_perplexity_answer  # ← FIXED: Added dot for relative import

app = FastAPI()

@app.get("/search")
def search(promt: str = Query(..., min_length=3)):
    try:
        answer = fetch_perplexity_answer(promt)
        return {"prompt": promt, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))

@app.get("/")
def root():
    return {"message": "Perplexity AI Agent is running! Use /search?promt=your_question"}
