from datetime import datetime
from typing import Optional, Dict, Any, List
from uuid import UUID

from pydantic import BaseModel, Field


class ToolConfig(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any]

def serialize_tool_config(tool_config: Dict[str, Dict[str, ToolConfig]]) -> Dict[str, Dict[str, Dict]]:
    """Convert a nested dictionary of ToolConfig objects into JSON-serializable dictionaries."""
    return {
        key: {sub_key: sub_value.dict() for sub_key, sub_value in sub_dict.items()}
        for key, sub_dict in tool_config.items()
    }

class AgentConfig(BaseModel):
    return_json: bool = Field(default=True)
    behavior_format_data: Optional[Dict[str, Any]] = None
    session_id: Optional[str] = None
    project_path: Optional[str] = None
    project_name: Optional[str] = None
    uses_tags: bool = Field(default=False)
    tag_response_index: str = Field(default="final_response")
    project_description: str = Field(default="None")
    agent_log_path: str = Field(default="agent_log")
    model_name: str = Field(default="gpt-4o-mini")
    call_type: str = Field(default="gpt")
    model_stop_token: Optional[str] = None
    temperature: float = Field(default=0.25, ge=0, le=1)
    max_tokens: int = Field(default=4000, gt=0)
    max_context_window: int = Field(default=100000, gt=0)
    frequency_penalty: float = Field(default=0.1, ge=0, le=2)
    presence_penalty: float = Field(default=0.1, ge=0, le=2)
    n: int = Field(default=1, gt=0)
    reset_on_x_tasks: int = Field(default=1, gt=0)
    agent_fields: List[str] = Field(default=["system", "user", "assistant"])
    message_append: Optional[str] = None
    model_loop_catcher_config: Optional[Dict[str, str]] = None

class AgentCreate(BaseModel):
    name: str
    agent_type: str
    tool_config: Dict[str, Dict[str, ToolConfig]]
    behavior: str
    config: AgentConfig

class AgentUpdate(BaseModel):
    name: Optional[str] = None
    agent_type: Optional[str] = None
    tool_config: Optional[Dict[str, Dict[str, ToolConfig]]] = None
    behavior: Optional[str] = None
    config: Optional[AgentConfig] = None
    is_active: Optional[bool] = None

class ImageInput(BaseModel):
    type: str = Field(..., description="Type of image input: 'base64', 'url', or 'path'")
    data: str = Field(..., description="Image data: base64 string, URL, or file path")

class AgentInteraction(BaseModel):
    message: str
    message_prefill: Optional[str] = None
    image: Optional[ImageInput] = None
    command_results: Optional[Dict[str, Any]] = Field(default=None, description='Results of commands executed, with command names as keys and their results as values')

class FunctionCall(BaseModel):
    function: str
    parameters: Dict[str, Any]
    sequence_id: int

class FunctionResult(BaseModel):
    sequence_id: int
    result: Any
    status: str = Field(..., pattern='^(success|error)$')
    error: Optional[str] = None

class AgentMemoryState(BaseModel):
    action_history: Dict[str, List[Any]]
    latest_action: Optional[str]
    latest_action_list: List[str]
    plan: str

class FunctionCallHistory(BaseModel):
    sequence_id: int
    function: str
    parameters: Dict[str, Any]
    result: Any
    status: str

class AgentResponse(BaseModel):
    response: Any
    metadata: Dict[str, Any] = Field(
        default_factory=lambda: {
            "latest_action": None,
            "latest_action_list": [],
            "plan": "None",
            "processing_time": 0.0,
            "memory_state": {
                "action_history": {},
                "latest_action": None,
                "latest_action_list": [],
                "plan": "None"
            },
            "function_calls": []
        }
    )

class Agent(BaseModel):
    id: UUID
    name: str
    agent_type: str
    tool_config: Dict[str, Dict[str, ToolConfig]]
    behavior: str
    config: AgentConfig
    user_id: UUID
    created_at: datetime
    last_used: Optional[datetime]
    is_active: bool

    class Config:
        from_attributes = True
