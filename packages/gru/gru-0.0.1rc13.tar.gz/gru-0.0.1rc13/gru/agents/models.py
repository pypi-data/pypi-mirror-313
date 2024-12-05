from pydantic import BaseModel
from typing import Dict, Any

class AgentPromptRequest(BaseModel):
    """
    Model representing a prompt request to an agent.
    
    Attributes:
        prompt (Dict[str, Any]): Dictionary containing the prompt data
    """
    prompt: Dict[str, Any]

class AgentRegisterRequest(BaseModel):
	cluster_name: str
	agent_name: str
	image: str
	image_pull_secret: str
	task_server_name: str
	checkpoint_db_name: str
	replicas: int
