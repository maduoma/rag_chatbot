from fastapi import FastAPI
from app.api import routes

app = FastAPI(title="RAG Chatbot API")

# Include API routes
app.include_router(routes.router)

# Health check endpoint
@app.get("/")
def health():
    return {"status": "ok"}
