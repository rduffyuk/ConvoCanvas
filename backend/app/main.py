from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.conversations import router as conversations_router
from app.api.enhanced_conversations import router as enhanced_conversations_router
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
app.include_router(conversations_router, prefix="/api/conversations", tags=["conversations"])
app.include_router(enhanced_conversations_router, prefix="/api/v2/conversations", tags=["enhanced-analysis"])

# Conditionally include GPU router only if GPU features are enabled
if feature_flags.is_enabled(Features.GPU_ACCELERATION):
    try:
        from app.api.gpu_conversations import router as gpu_conversations_router
        app.include_router(gpu_conversations_router, prefix="/api/v3/conversations", tags=["gpu-acceleration"])
    except ImportError as e:
        print(f"GPU features disabled due to missing dependencies: {e}")

@app.get("/")
async def root():
    endpoints = {
        "legacy": "/api/conversations/",
        "enhanced": "/api/v2/conversations/",
        "health": "/api/v2/conversations/health"
    }

    # Add GPU endpoints only if GPU acceleration is enabled
    if feature_flags.is_enabled(Features.GPU_ACCELERATION):
        endpoints.update({
            "gpu_accelerated": "/api/v3/conversations/",
            "gpu_status": "/api/v3/conversations/gpu-status"
        })

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
        "endpoints": endpoints,
        "feature_flags": feature_flags.get_config()
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "version": "0.2.0"}

@app.get("/feature-flags")
async def get_feature_flags():
    return {"feature_flags": feature_flags.get_config()}
