"""GPU-Enhanced conversation analysis API endpoints"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Response
from typing import Dict, Any
import json

from app.core.gpu_analyzer_integration import GPUEnhancedContentAnalyzer
from app.core.conversation_parser import ConversationParser
from app.core.canvas_generator import CanvasDecisionVisualizer, ExcalidrawDecisionVisualizer

router = APIRouter(prefix="/api/v3/conversations", tags=["GPU-Enhanced Conversations"])

@router.post("/analyze-gpu")
async def analyze_conversation_gpu_enhanced(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    GPU-accelerated conversation analysis with AI-powered insights and decision tracking

    Returns:
    - GPU-accelerated processing metrics
    - Enhanced technical decisions with confidence scores
    - GPU-computed text features and complexity metrics
    - AI-powered content suggestions
    - Sentiment analysis
    - Named entity recognition
    - Technical domain classification
    """
    try:
        # Read and parse file
        content = await file.read()
        text_content = content.decode('utf-8')

        # Initialize GPU-enhanced analyzer
        analyzer = GPUEnhancedContentAnalyzer()

        # Extract structured dialogue with GPU acceleration
        messages_result = analyzer.extract_user_claude_dialogue(text_content)

        if not messages_result.get('messages'):
            raise HTTPException(status_code=400, detail="No valid conversation content found")

        # Extract decisions with GPU insights
        decisions_result = analyzer.extract_decisions(messages_result)

        # Generate enhanced content ideas (CPU-based but enhanced with GPU data)
        content_ideas = analyzer.generate_enhanced_content_ideas(
            messages_result.get('messages', []),
            decisions_result.get('decisions', [])
        )

        # Create comprehensive response with GPU metrics
        response = {
            "conversation_analysis": {
                "total_messages": len(messages_result.get('messages', [])),
                "total_decisions": len(decisions_result.get('decisions', [])),
                "gpu_enhanced": messages_result.get('gpu_enhanced', False),
                "processing_method": messages_result.get('processing_method', 'unknown'),
                "gpu_processing_time": messages_result.get('gpu_processing_time', 0),
                "gpu_features": messages_result.get('gpu_features', {}),
                "gpu_entities": messages_result.get('gpu_entities', []),
                "gpu_key_phrases": messages_result.get('gpu_key_phrases', [])
            },
            "messages": messages_result.get('messages', []),
            "decisions": {
                "cpu_decisions": decisions_result.get('decisions', []),
                "gpu_decisions": decisions_result.get('gpu_decisions', []),
                "gpu_action_items": decisions_result.get('gpu_action_items', [])
            },
            "content_ideas": content_ideas,
            "metadata": {
                "filename": file.filename,
                "file_size": len(text_content),
                "gpu_acceleration": analyzer.gpu_available,
                "analyzer_type": "gpu_enhanced_v3"
            }
        }

        return response

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing conversation: {str(e)}"
        )

@router.get("/gpu-status")
async def get_gpu_analyzer_status() -> Dict[str, Any]:
    """Get current GPU analyzer system status"""
    try:
        analyzer = GPUEnhancedContentAnalyzer()
        status = analyzer.get_system_status()

        return {
            "status": "healthy",
            "gpu_details": status,
            "api_version": "v3",
            "features": {
                "gpu_acceleration": status.get('gpu_available', False),
                "spacy_loaded": status.get('spacy_loaded', False),
                "hybrid_processing": True
            }
        }

    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "api_version": "v3",
            "features": {
                "gpu_acceleration": False,
                "spacy_loaded": False,
                "hybrid_processing": False
            }
        }

@router.post("/analyze-gpu-mindmap")
async def create_gpu_enhanced_mindmap(file: UploadFile = File(...)) -> Response:
    """
    Create GPU-enhanced decision mindmap visualization

    Returns an Excalidraw-compatible JSON visualization enhanced with GPU insights
    """
    try:
        # Read and parse file
        content = await file.read()
        text_content = content.decode('utf-8')

        # Initialize GPU-enhanced analyzer
        analyzer = GPUEnhancedContentAnalyzer()

        # Extract data with GPU acceleration
        messages_result = analyzer.extract_user_claude_dialogue(text_content)
        decisions_result = analyzer.extract_decisions(messages_result)

        # Create enhanced mindmap with GPU insights
        visualizer = ExcalidrawDecisionVisualizer()

        # Combine CPU and GPU decisions for comprehensive visualization
        all_decisions = decisions_result.get('decisions', [])
        gpu_decisions = decisions_result.get('gpu_decisions', [])
        gpu_actions = decisions_result.get('gpu_action_items', [])

        # Create enhanced decision data
        enhanced_decisions = all_decisions.copy()

        # Add GPU-detected decisions
        for gpu_decision in gpu_decisions:
            enhanced_decisions.append({
                'decision': gpu_decision.get('decision_text', ''),
                'confidence': gpu_decision.get('confidence', 0.5),
                'context': gpu_decision.get('position', 0),
                'type': 'gpu_detected'
            })

        # Add GPU action items as decisions
        for action in gpu_actions:
            enhanced_decisions.append({
                'decision': action.get('action_text', ''),
                'confidence': action.get('confidence', 0.7),
                'context': action.get('position', 0),
                'type': 'action_item',
                'priority': action.get('priority', 'medium')
            })

        # Generate mindmap with enhanced data
        mindmap_json = visualizer.create_decision_mindmap(
            enhanced_decisions,
            title=f"GPU-Enhanced Analysis: {file.filename}"
        )

        # Add GPU metadata to the mindmap
        mindmap_data = json.loads(mindmap_json)
        mindmap_data['gpu_enhanced'] = True
        mindmap_data['processing_method'] = messages_result.get('processing_method', 'unknown')
        mindmap_data['gpu_features'] = messages_result.get('gpu_features', {})

        return Response(
            content=json.dumps(mindmap_data, indent=2),
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename={file.filename}_gpu_mindmap.json"}
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error creating GPU-enhanced mindmap: {str(e)}"
        )

@router.post("/analyze-gpu-performance")
async def analyze_gpu_performance(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Performance comparison between CPU and GPU processing
    """
    try:
        import time

        # Read content
        content = await file.read()
        text_content = content.decode('utf-8')

        # Test GPU-enhanced analyzer
        start_time = time.time()
        gpu_analyzer = GPUEnhancedContentAnalyzer()
        gpu_messages = gpu_analyzer.extract_user_claude_dialogue(text_content)
        gpu_decisions = gpu_analyzer.extract_decisions(gpu_messages)
        gpu_time = time.time() - start_time

        # Test original CPU analyzer (for comparison)
        from app.core.enhanced_content_analyzer import EnhancedContentAnalyzer
        start_time = time.time()
        cpu_analyzer = EnhancedContentAnalyzer()
        cpu_messages = cpu_analyzer.extract_user_claude_dialogue(text_content)
        cpu_decisions = cpu_analyzer.extract_decisions(cpu_messages)
        cpu_time = time.time() - start_time

        # Performance metrics
        speedup = cpu_time / gpu_time if gpu_time > 0 else 1.0

        return {
            "performance_comparison": {
                "gpu_processing_time": gpu_time,
                "cpu_processing_time": cpu_time,
                "speedup_factor": speedup,
                "gpu_memory_used": gpu_messages.get('gpu_features', {}).get('gpu_memory_used_mb', 0)
            },
            "content_analysis": {
                "file_size": len(text_content),
                "gpu_messages_found": len(gpu_messages.get('messages', [])),
                "cpu_messages_found": len(cpu_messages),
                "gpu_decisions": len(gpu_decisions.get('decisions', [])),
                "cpu_decisions": len(cpu_decisions),
                "gpu_entities": len(gpu_messages.get('gpu_entities', [])),
                "gpu_key_phrases": len(gpu_messages.get('gpu_key_phrases', []))
            },
            "recommendations": {
                "use_gpu": speedup > 1.1,
                "reason": f"GPU is {speedup:.2f}x faster" if speedup > 1.1 else f"CPU is {1/speedup:.2f}x faster"
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing performance: {str(e)}"
        )