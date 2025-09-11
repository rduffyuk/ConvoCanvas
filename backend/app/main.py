from fastapi import FastAPI
from app.api.conversations import router as conversations_router

app = FastAPI(title="ConvoCanvas API", version="0.1.0")
app.include_router(conversations_router, prefix="/api/conversations", tags=["conversations"])

@app.get("/")
async def root():
    return {"message": "ConvoCanvas API is running"}
