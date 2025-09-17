from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.app.api.conversations import router as conversations_router
from app.core.app.api.enhanced_conversations import router as enhanced_conversations_router
from app.api.gpu_conversations import router as gpu_conversations_router
from app.core.feature_flags import feature_flags, Features

app = FastAPI(
    title="ConvoCanvas API",
    version="0.2.0-alpha",
    description="AI-powered conversation analysis with decision tracking and visual insights"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://convocanvas.uk"],  # Next.js dev + production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(conversations_router, tags=["conversations"])
app.include_router(enhanced_conversations_router, tags=["enhanced-analysis"])
app.include_router(gpu_conversations_router, tags=["gpu-acceleration"])

@app.get("/")
async def root():
    return {
        "message": "ConvoCanvas API v0.2.0-alpha - Enhanced Analysis Ready",
        "features": [
            "AI-powered conversation analysis",
            "Technical decision extraction",
            "Interactive decision mindmaps",
            "Sentiment analysis",
            "Named entity recognition",
            "Enhanced content generation"
        ],
        "endpoints": {
            "legacy": "/api/conversations/",
            "enhanced": "/api/v2/conversations/",
            "gpu_accelerated": "/api/v3/conversations/",
            "health": "/api/v2/conversations/health",
            "gpu_status": "/api/v3/conversations/gpu-status"
        }
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "version": "0.2.0"}
