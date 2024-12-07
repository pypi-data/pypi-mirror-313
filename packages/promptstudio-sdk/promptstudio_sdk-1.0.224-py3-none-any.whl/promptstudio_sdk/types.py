from typing import Optional, List, Dict
from enum import Enum
from pydantic import BaseModel


class MessageType(str, Enum):
    TEXT = "text"
    FILE = "file"


class Memory(str, Enum):
    FULL_MEMORY = "fullMemory"
    WINDOW_MEMORY = "windowMemory"
    SUMMARIZED_MEMORY = "summarizedMemory"


class FileUrl(BaseModel):
    url: str


class MessageContent(BaseModel):
    type: MessageType
    text: Optional[str] = None
    file_url: Optional[FileUrl] = None


class Message(BaseModel):
    role: str
    content: List[MessageContent]


class RequestPayload(BaseModel):
    user_message: List[MessageContent]
    memory_type: Memory
    window_size: int
    session_id: str
    variables: Dict[str, str]
    version: Optional[float] = None


class AIPlatform(BaseModel):
    platform: str
    model: str
    temp: float
    max_tokens: int
    top_p: float
    frequency_penalty: float
    presence_penalty: float
    top_k: Optional[int] = None
    response_format: Optional[Dict[str, str]] = None


class PromptDetail(BaseModel):
    id: str
    ai_platform: AIPlatform
    version: float
    is_published: bool
    is_image_support: bool
    is_audio_support: bool


class PromptResponse(BaseModel):
    response: str
