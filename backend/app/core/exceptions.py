from fastapi import HTTPException, status
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class ConvoCanvasException(Exception):
    """Base exception for ConvoCanvas application"""
    def __init__(self, message: str, details: Optional[str] = None):
        self.message = message
        self.details = details
        super().__init__(self.message)

class FileProcessingError(ConvoCanvasException):
    """Raised when file processing fails"""
    pass

class UnsupportedFileTypeError(ConvoCanvasException):
    """Raised when unsupported file type is uploaded"""
    pass

class ContentAnalysisError(ConvoCanvasException):
    """Raised when content analysis fails"""
    pass

class ParsingError(ConvoCanvasException):
    """Raised when conversation parsing fails"""
    pass

def handle_file_processing_error(error: Exception, filename: str) -> HTTPException:
    """Convert file processing errors to HTTP exceptions with proper logging"""
    logger.error(f"File processing error for {filename}: {str(error)}", exc_info=True)

    if isinstance(error, UnsupportedFileTypeError):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "unsupported_file_type",
                "message": f"File type not supported: {filename}",
                "details": str(error)
            }
        )
    elif isinstance(error, ParsingError):
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error": "parsing_failed",
                "message": f"Failed to parse conversation file: {filename}",
                "details": str(error)
            }
        )
    elif isinstance(error, ContentAnalysisError):
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error": "analysis_failed",
                "message": f"Failed to analyze content: {filename}",
                "details": str(error)
            }
        )
    elif isinstance(error, FileProcessingError):
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "file_processing_failed",
                "message": f"Unable to process file: {filename}",
                "details": str(error)
            }
        )
    else:
        # Generic server error for unexpected exceptions
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "internal_server_error",
                "message": "An unexpected error occurred while processing the file",
                "details": "Please try again or contact support if the problem persists"
            }
        )