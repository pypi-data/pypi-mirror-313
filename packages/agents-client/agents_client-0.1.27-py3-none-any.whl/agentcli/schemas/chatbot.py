from datetime import datetime
from typing import Optional, Dict, Any
from uuid import UUID

from pydantic import BaseModel, Field


class ChatbotConfig(BaseModel):
    temperature: float = Field(default=0.7, ge=0, le=1)
    max_tokens: int = Field(default=4000, gt=0)
    max_context_window: int = Field(default=100000, gt=0)
    provider: str = Field(default="openai")
    model_stop_token: Optional[str] = None
    frequency_penalty: float = Field(default=0.1, ge=0, le=2)
    presence_penalty: float = Field(default=0.1, ge=0, le=2)
    n: int = Field(default=1, gt=0)
    behavior: Optional[str] = None
    return_json: bool = Field(default=False)
    agent_fields: list[str] = Field(default=["system", "user", "assistant"])

class ImageInput(BaseModel):
    type: str = Field(..., description="Type of image input: 'base64', 'url', or 'path'")
    data: str = Field(..., description="Image data: base64 string, URL, or file path")

class ChatbotCreate(BaseModel):
    name: str
    model: str
    config: ChatbotConfig

class ChatbotUpdate(BaseModel):
    name: Optional[str] = None
    model: Optional[str] = None
    config: Optional[ChatbotConfig] = None
    is_active: Optional[bool] = None

class ChatbotInference(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None
    image: Optional[ImageInput] = None
    add_to_history: bool = True
    message_prefill: Optional[str] = None

class ChatbotResponse(BaseModel):
    response: str
    metadata: Dict[str, Any] = Field(
        default_factory=lambda: {
            "model_used": "",
            "tokens": {
                "total_tokens": 0,
                "input_tokens": 0,
                "output_tokens": 0,
                "system_tokens": 0
            },
            "processing_time": 0.0,
            "history_length": 0
        }
    )

class Chatbot(BaseModel):
    id: UUID
    name: str
    model: str
    config: ChatbotConfig
    user_id: UUID
    created_at: datetime
    last_used: Optional[datetime]
    is_active: bool

    class Config:
        from_attributes = True
