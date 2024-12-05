from abc import ABC, abstractmethod
from typing import Any

from gru.agents.schemas import AgentInvokeRequest
from gru.agents.schemas.schemas import TaskCompleteRequest


class AgentWorkflow(ABC):

    @abstractmethod
    async def setup(self):
        pass
    
    @abstractmethod
    async def invoke(self, request: AgentInvokeRequest) -> dict[str, Any]:
        pass

    @abstractmethod
    async def resume(self, request: TaskCompleteRequest) -> dict[str, Any]:
        pass