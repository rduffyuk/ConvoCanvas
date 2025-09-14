from fastapi import APIRouter, UploadFile, File, HTTPException
from app.core.conversation_parser import parse_file
import tempfile
import os

router = APIRouter()

# Maximum file size (10MB)
MAX_FILE_SIZE = 10 * 1024 * 1024
ALLOWED_EXTENSIONS = {".md", ".txt"}


@router.post("/upload")
async def upload_conversation(file: UploadFile = File(...)):
    """Upload and parse a conversation file."""
    # Validate file extension
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Only {', '.join(ALLOWED_EXTENSIONS)} files supported",
        )

    # Read and validate file content
    content = await file.read()

    # Validate file size
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {MAX_FILE_SIZE // 1024 // 1024}MB",
        )

    # Validate content is not empty
    if not content.strip():
        raise HTTPException(status_code=400, detail="File is empty")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".md") as tmp_file:
        tmp_file.write(content)
        tmp_file_path = tmp_file.name

    try:
        result = parse_file(tmp_file_path)
        return {
            "filename": file.filename,
            "title": result.title,
            "source": result.source,
            "word_count": result.word_count,
            "status": "parsed_successfully",
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid file format: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Parsing failed: {str(e)}")
    finally:
        if os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)


@router.post("/analyze")
async def analyze_conversation_content(file: UploadFile = File(...)):
    """Analyze conversation content for insights."""
    from app.core.content_analyzer import extract_content_ideas

    # Validate file extension
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Only {', '.join(ALLOWED_EXTENSIONS)} files supported",
        )

    # Read and validate file content
    content = await file.read()

    # Validate file size
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large. Maximum size is {MAX_FILE_SIZE // 1024 // 1024}MB",
        )

    # Validate content is not empty
    if not content.strip():
        raise HTTPException(status_code=400, detail="File is empty")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".md") as tmp_file:
        tmp_file.write(content)
        tmp_file_path = tmp_file.name

    try:
        with open(tmp_file_path, "r", encoding="utf-8") as f:
            content_str = f.read()

        if not content_str.strip():
            raise HTTPException(status_code=400, detail="File content is empty")

        ideas = extract_content_ideas(content_str)
        return {"analysis": ideas, "status": "analysis_complete"}
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400, detail="File encoding not supported. Please use UTF-8."
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid file content: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    finally:
        if os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)
