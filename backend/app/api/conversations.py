from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.core.conversation_parser import parse_file
from app.core.exceptions import (
    handle_file_processing_error,
    UnsupportedFileTypeError,
    ParsingError,
    FileProcessingError
)
from app.models import ConversationParseResult, ContentAnalysisResult
import tempfile
import os
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/upload", response_model=ConversationParseResult)
async def upload_conversation(file: UploadFile = File(...)):
    """Upload and parse a conversation file (.md or .txt)"""

    # Validate file type
    if not file.filename or not file.filename.lower().endswith(('.md', '.txt')):
        raise handle_file_processing_error(
            UnsupportedFileTypeError("Only .md and .txt files are supported"),
            file.filename or "unknown"
        )

    # Validate file size (10MB limit)
    if file.size and file.size > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail={
                "error": "file_too_large",
                "message": "File size exceeds 10MB limit",
                "details": f"File size: {file.size} bytes"
            }
        )

    tmp_file_path = None

    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.md') as tmp_file:
            content = await file.read()
            if not content:
                raise FileProcessingError("File appears to be empty")

            tmp_file.write(content)
            tmp_file_path = tmp_file.name

        # Parse the file
        result = parse_file(tmp_file_path)

        logger.info(f"Successfully parsed file: {file.filename}")

        return ConversationParseResult(
            filename=file.filename,
            title=result.title if hasattr(result, 'title') else None,
            source=result.source if hasattr(result, 'source') else None,
            word_count=result.word_count if hasattr(result, 'word_count') else 0
        )

    except Exception as e:
        if isinstance(e, (UnsupportedFileTypeError, ParsingError, FileProcessingError)):
            raise handle_file_processing_error(e, file.filename)
        else:
            # Wrap unexpected errors
            raise handle_file_processing_error(
                ParsingError(f"Unexpected parsing error: {str(e)}"),
                file.filename
            )
    finally:
        # Clean up temporary file
        if tmp_file_path and os.path.exists(tmp_file_path):
            try:
                os.unlink(tmp_file_path)
            except Exception as cleanup_error:
                logger.warning(f"Failed to cleanup temp file {tmp_file_path}: {cleanup_error}")

@router.post("/analyze", response_model=ContentAnalysisResult)
async def analyze_conversation_content(file: UploadFile = File(...)):
    """Analyze conversation content to extract ideas and insights"""

    from app.core.content_analyzer import extract_content_ideas
    from app.core.exceptions import ContentAnalysisError
    from app.models import ContentAnalysisResult

    # Validate file type
    if not file.filename or not file.filename.lower().endswith(('.md', '.txt')):
        raise handle_file_processing_error(
            UnsupportedFileTypeError("Only .md and .txt files are supported"),
            file.filename or "unknown"
        )

    # Validate file size
    if file.size and file.size > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail={
                "error": "file_too_large",
                "message": "File size exceeds 10MB limit",
                "details": f"File size: {file.size} bytes"
            }
        )

    tmp_file_path = None

    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.md') as tmp_file:
            content = await file.read()
            if not content:
                raise FileProcessingError("File appears to be empty")

            tmp_file.write(content)
            tmp_file_path = tmp_file.name

        # Read and analyze content
        with open(tmp_file_path, 'r', encoding='utf-8') as f:
            content_str = f.read()

        if not content_str.strip():
            raise ContentAnalysisError("File contains no readable text content")

        ideas = extract_content_ideas(content_str)

        logger.info(f"Successfully analyzed file: {file.filename}")

        return ContentAnalysisResult(
            analysis=ideas if isinstance(ideas, list) else [str(ideas)],
            status="analysis_complete"
        )

    except Exception as e:
        if isinstance(e, (UnsupportedFileTypeError, ContentAnalysisError, FileProcessingError)):
            raise handle_file_processing_error(e, file.filename)
        else:
            # Wrap unexpected errors
            raise handle_file_processing_error(
                ContentAnalysisError(f"Unexpected analysis error: {str(e)}"),
                file.filename
            )
    finally:
        # Clean up temporary file
        if tmp_file_path and os.path.exists(tmp_file_path):
            try:
                os.unlink(tmp_file_path)
            except Exception as cleanup_error:
                logger.warning(f"Failed to cleanup temp file {tmp_file_path}: {cleanup_error}")
