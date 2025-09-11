from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.conversation_parser import parse_file
import tempfile
import os

router = APIRouter()

@router.post("/upload")
async def upload_conversation(file: UploadFile = File(...)):
    if not file.filename.endswith(('.md', '.txt')):
        raise HTTPException(status_code=400, detail="Only .md and .txt files supported")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.md') as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_file_path = tmp_file.name
    
    try:
        result = parse_file(tmp_file_path)
        return {
            "filename": file.filename,
            "title": result.title,
            "source": result.source,
            "word_count": result.word_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Parsing failed: {str(e)}")
    finally:
        os.unlink(tmp_file_path)

@router.post("/analyze")
async def analyze_conversation_content(file: UploadFile = File(...)):
    from app.core.content_analyzer import extract_content_ideas
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.md') as tmp_file:
        content = await file.read()
        tmp_file.write(content)
        tmp_file_path = tmp_file.name
    
    try:
        with open(tmp_file_path, 'r', encoding='utf-8') as f:
            content_str = f.read()
        ideas = extract_content_ideas(content_str)
        return {"analysis": ideas, "status": "analysis_complete"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    finally:
        os.unlink(tmp_file_path)
