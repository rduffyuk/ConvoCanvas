from pydantic import BaseModel, Field, validator
from typing import Optional, List
from enum import Enum

class FileType(str, Enum):
    MARKDOWN = "md"
    TEXT = "txt"

class ConversationParseResult(BaseModel):
    filename: str = Field(..., description="Original filename")
    title: Optional[str] = Field(None, description="Extracted conversation title")
    source: Optional[str] = Field(None, description="Conversation source/platform")
    word_count: int = Field(0, ge=0, description="Number of words in conversation")

class ContentAnalysisResult(BaseModel):
    analysis: List[str] = Field(default_factory=list, description="Extracted content ideas")
    status: str = Field("analysis_complete", description="Analysis completion status")

class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Human-readable error message")
    details: Optional[str] = Field(None, description="Additional error details")

class UploadFileRequest(BaseModel):
    filename: str = Field(..., description="Name of the uploaded file")

    @validator('filename')
    def validate_file_extension(cls, v):
        if not v.lower().endswith(('.md', '.txt')):
            raise ValueError('Only .md and .txt files are supported')
        return v