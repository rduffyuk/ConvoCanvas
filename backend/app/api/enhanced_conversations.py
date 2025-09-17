"""Enhanced conversation analysis API with decision tracking and visualization"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Response
from typing import Dict, Any
import json

from app.core.enhanced_content_analyzer import EnhancedContentAnalyzer
from app.core.conversation_parser import ConversationParser
from app.core.canvas_generator import CanvasDecisionVisualizer, ExcalidrawDecisionVisualizer

router = APIRouter(tags=["Enhanced Conversations"])

@router.post("/analyze-enhanced")
async def analyze_conversation_enhanced(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Enhanced conversation analysis with AI-powered insights and decision tracking

    Returns:
    - Technical decisions with confidence scores
    - Interactive decision mindmap
    - AI-powered content suggestions
    - Sentiment analysis
    - Named entity recognition
    - Technical domain classification
    """
    try:
        # Read and parse file
        content = await file.read()
        text_content = content.decode('utf-8')

        # Initialize enhanced analyzer
        analyzer = EnhancedContentAnalyzer()

        # Extract structured dialogue
        messages = analyzer.extract_user_claude_dialogue(text_content)

        if not messages:
            raise HTTPException(status_code=400, detail="No valid conversation content found")

        # Extract decisions with AI
        decisions = analyzer.extract_decisions(messages)

        # Create decision mindmap
        mindmap_data = analyzer.create_decision_mindmap(decisions)

        # Generate enhanced content ideas
        content_ideas = analyzer.generate_enhanced_content_ideas(messages, decisions)

        # Compile comprehensive response
        response = {
            "analysis_type": "enhanced",
            "conversation_metadata": {
                "filename": file.filename,
                "total_messages": len(messages),
                "user_messages": len([m for m in messages if m['role'] == 'user']),
                "claude_messages": len([m for m in messages if m['role'] == 'claude']),
                "average_sentiment": sum(m['sentiment']['polarity'] for m in messages) / len(messages) if messages else 0
            },
            "decisions": {
                "extracted_decisions": decisions,
                "decision_mindmap": mindmap_data,
                "summary": mindmap_data.get("summary", {})
            },
            "content_analysis": content_ideas,
            "technical_insights": {
                "dominant_domains": content_ideas.get('conversation_themes', []),
                "key_entities": _extract_top_entities(messages),
                "sentiment_flow": content_ideas.get('sentiment_analysis', {}),
                "technical_concepts": content_ideas.get('technical_concepts', [])
            },
            "recommendations": _generate_recommendations(decisions, content_ideas, messages)
        }

        return response

    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File encoding not supported. Please use UTF-8.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.post("/decisions/extract")
async def extract_decisions_only(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Extract only technical decisions from conversation for decision tracking
    """
    try:
        content = await file.read()
        text_content = content.decode('utf-8')

        analyzer = EnhancedContentAnalyzer()
        messages = analyzer.extract_user_claude_dialogue(text_content)
        decisions = analyzer.extract_decisions(messages)
        mindmap_data = analyzer.create_decision_mindmap(decisions)

        return {
            "decisions": decisions,
            "mindmap": mindmap_data,
            "decision_summary": {
                "total_decisions": len(decisions),
                "high_confidence": len([d for d in decisions if d['confidence'] > 0.7]),
                "by_role": {
                    "user_decisions": len([d for d in decisions if d['role'] == 'user']),
                    "claude_decisions": len([d for d in decisions if d['role'] == 'claude'])
                },
                "technical_domains": list(set().union(*[d['technical_domains'] for d in decisions if d['technical_domains']]))
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Decision extraction failed: {str(e)}")

@router.post("/mindmap/generate")
async def generate_decision_mindmap(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Generate interactive decision mindmap visualization
    """
    try:
        content = await file.read()
        text_content = content.decode('utf-8')

        analyzer = EnhancedContentAnalyzer()
        messages = analyzer.extract_user_claude_dialogue(text_content)
        decisions = analyzer.extract_decisions(messages)
        mindmap_data = analyzer.create_decision_mindmap(decisions)

        return {
            "mindmap_html": mindmap_data["html"],
            "nodes": mindmap_data["nodes"],
            "edges": mindmap_data["edges"],
            "summary": mindmap_data["summary"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Mindmap generation failed: {str(e)}")

@router.post("/canvas/generate")
async def generate_decision_canvas(file: UploadFile = File(...)) -> Response:
    """
    Generate Obsidian Canvas file for decision visualization

    Returns:
    Canvas JSON file for import into Obsidian
    """
    try:
        content = await file.read()
        text_content = content.decode('utf-8')

        analyzer = EnhancedContentAnalyzer()
        messages = analyzer.extract_user_claude_dialogue(text_content)
        decisions = analyzer.extract_decisions(messages)

        # Generate Canvas
        canvas_generator = CanvasDecisionVisualizer()
        conversation_title = file.filename.replace('.md', '').replace('-', ' ').title() if file.filename else "Decision Flow"
        canvas_json = canvas_generator.create_decision_canvas(decisions, conversation_title)

        return Response(
            content=canvas_json,
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename={conversation_title.replace(' ', '-')}-decision-flow.canvas"}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Canvas generation failed: {str(e)}")

@router.post("/excalidraw/generate")
async def generate_decision_excalidraw(file: UploadFile = File(...)) -> Response:
    """
    Generate Excalidraw file for decision visualization

    Returns:
    .excalidraw.md file for use in Obsidian with Excalidraw plugin
    """
    try:
        content = await file.read()
        text_content = content.decode('utf-8')

        analyzer = EnhancedContentAnalyzer()
        messages = analyzer.extract_user_claude_dialogue(text_content)
        decisions = analyzer.extract_decisions(messages)

        # Generate Excalidraw
        excalidraw_generator = ExcalidrawDecisionVisualizer()
        conversation_title = file.filename.replace('.md', '').replace('-', ' ').title() if file.filename else "Decision Flow"
        excalidraw_content = excalidraw_generator.create_decision_excalidraw(decisions, conversation_title)

        return Response(
            content=excalidraw_content,
            media_type="text/markdown",
            headers={"Content-Disposition": f"attachment; filename={conversation_title.replace(' ', '-')}-decision-flow.excalidraw.md"}
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Excalidraw generation failed: {str(e)}")

@router.post("/obsidian/visualize")
async def generate_obsidian_visualizations(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    Generate all Obsidian-compatible visualizations for decisions

    Returns:
    JSON with Canvas and Excalidraw content for manual file creation
    """
    try:
        content = await file.read()
        text_content = content.decode('utf-8')

        analyzer = EnhancedContentAnalyzer()
        messages = analyzer.extract_user_claude_dialogue(text_content)
        decisions = analyzer.extract_decisions(messages)

        conversation_title = file.filename.replace('.md', '').replace('-', ' ').title() if file.filename else "Decision Flow"

        # Generate both formats
        canvas_generator = CanvasDecisionVisualizer()
        excalidraw_generator = ExcalidrawDecisionVisualizer()

        canvas_content = canvas_generator.create_decision_canvas(decisions, conversation_title)
        excalidraw_content = excalidraw_generator.create_decision_excalidraw(decisions, conversation_title)

        return {
            "conversation_title": conversation_title,
            "decisions_found": len(decisions),
            "visualizations": {
                "canvas": {
                    "filename": f"{conversation_title.replace(' ', '-')}-decision-flow.canvas",
                    "content": canvas_content
                },
                "excalidraw": {
                    "filename": f"{conversation_title.replace(' ', '-')}-decision-flow.excalidraw.md",
                    "content": excalidraw_content
                }
            },
            "decision_summary": {
                "total_decisions": len(decisions),
                "by_role": {
                    "user": len([d for d in decisions if d.get('role') == 'user']),
                    "assistant": len([d for d in decisions if d.get('role') == 'assistant'])
                },
                "average_confidence": sum(d.get('confidence', 0) for d in decisions) / len(decisions) if decisions else 0
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Obsidian visualization generation failed: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check for enhanced analyzer"""
    try:
        analyzer = EnhancedContentAnalyzer()
        return {
            "status": "healthy",
            "nlp_model_loaded": analyzer.nlp is not None,
            "features": [
                "decision_extraction",
                "sentiment_analysis",
                "entity_recognition",
                "mindmap_visualization",
                "ai_content_generation"
            ]
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

def _extract_top_entities(messages, limit=10):
    """Extract top named entities across all messages"""
    all_entities = []
    for message in messages:
        all_entities.extend(message.get('entities', []))

    # Count entity occurrences
    entity_counts = {}
    for entity in all_entities:
        key = f"{entity['text']}_{entity['label']}"
        if key not in entity_counts:
            entity_counts[key] = {
                "text": entity['text'],
                "label": entity['label'],
                "description": entity['description'],
                "count": 0
            }
        entity_counts[key]["count"] += 1

    # Return top entities by frequency
    sorted_entities = sorted(entity_counts.values(), key=lambda x: x['count'], reverse=True)
    return sorted_entities[:limit]

def _generate_recommendations(decisions, content_ideas, messages):
    """Generate actionable recommendations based on analysis"""
    recommendations = []

    # Decision-based recommendations
    if decisions:
        high_conf_decisions = [d for d in decisions if d['confidence'] > 0.7]
        if len(high_conf_decisions) < len(decisions) * 0.5:
            recommendations.append({
                "type": "decision_clarity",
                "priority": "medium",
                "message": "Consider being more explicit about final decisions in conversations",
                "action": "Use phrases like 'final decision:', 'we will:', or 'conclusion:'"
            })

    # Content generation recommendations
    sentiment = content_ideas.get('sentiment_analysis', {})
    if sentiment.get('overall_sentiment') == 'negative':
        recommendations.append({
            "type": "content_tone",
            "priority": "low",
            "message": "Conversation has negative sentiment - consider highlighting positive outcomes",
            "action": "Focus on solutions and achievements in generated content"
        })

    # Technical depth recommendations
    if len(content_ideas.get('conversation_themes', [])) > 3:
        recommendations.append({
            "type": "focus",
            "priority": "medium",
            "message": "Conversation covers many technical domains - consider focused follow-ups",
            "action": "Break complex multi-domain discussions into focused sessions"
        })

    return recommendations