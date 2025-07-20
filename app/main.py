from fastapi import FastAPI, HTTPException, Query
from .browser import fetch_perplexity_answer  # ← FIXED: Added dot for relative import
import traceback

app = FastAPI()

@app.get("/search")
def search(prompt: str = Query(..., min_length=3)):
    try:
        answer = fetch_perplexity_answer(prompt)
        return {"prompt": prompt, "answer": answer}
    except Exception as e:
        print("Error:", e)
        traceback.print_exc() 
        raise HTTPException(status_code=502, detail=str(e))

@app.get("/")
def root():
    return {"message": "Perplexity AI Agent is running! Use /search?promt=your_question"}
