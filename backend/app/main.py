from fastapi import FastAPI
from app.api.conversations import router as conversations_router

app = FastAPI(
    title="ConvoCanvas API",
    version="0.1.0",
    description="Transform AI conversations into actionable content insights",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(
    conversations_router, prefix="/api/conversations", tags=["conversations"]
)


@app.get("/", tags=["health"])
async def root():
    """Health check endpoint."""
    return {
        "message": "ConvoCanvas API is running",
        "version": "0.1.0",
        "status": "healthy",
    }


@app.get("/health", tags=["health"])
async def health_check():
    """Detailed health check endpoint."""
    return {
        "status": "healthy",
        "version": "0.1.0",
        "service": "ConvoCanvas API",
    }
