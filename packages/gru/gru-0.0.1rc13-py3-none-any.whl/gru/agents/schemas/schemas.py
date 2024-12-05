from typing import Any
from pydantic import BaseModel


class AgentInvokeRequest(BaseModel):
    prompt_id : str
    prompt_body : dict[str, Any]

class AgentInvokeResponse(BaseModel):
    prompt_id : str

class TaskCompleteRequest(BaseModel):
    prompt_id:str
    tool_call_id: str
    task_type: str
    status: str
    result: dict[str, Any]