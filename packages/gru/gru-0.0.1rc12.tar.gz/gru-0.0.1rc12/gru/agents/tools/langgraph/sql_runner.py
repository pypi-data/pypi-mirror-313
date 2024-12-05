import os
from typing import Any, Optional, Type, Union, cast
from langchain_core.tools import BaseTool
from langchain_core.callbacks import CallbackManagerForToolRun
from pydantic import BaseModel, Field
from langgraph.errors import NodeInterrupt
from langchain_core.runnables import RunnableConfig
from langchain_core.messages.tool import ToolCall

from gru.agents.task_server.celery import TaskMetadata, submit_task

class CansoSQLRunnerToolInput(BaseModel):
    query: str = Field(description="sql query to execute")

class CansoSQLRunnerTool(BaseTool):
    name: str = "run_sql_query"
    description: str = "Used to run sql queries on the database"
    args_schema: Type[BaseModel] = CansoSQLRunnerToolInput
    return_direct: bool = True

    class Config:
      extra = 'allow'

    # Note: This is still a crude implementation, Needs improvement

    def __init__(self, db_host, db_port, db_username, db_password, db_name):
        super().__init__(
            db_host = db_host,
            db_port = db_port,
            db_username = db_username,
            db_password = db_password,
            db_name = db_name,
            tool_call_id = ""
        )
        self.db_host = db_host
        self.db_port = db_port
        self.db_username = db_username
        self.db_password = db_password
        self.db_name = db_name
        self.tool_call_id = ""

    async def ainvoke(
        self,
        input: Union[str, dict, ToolCall],
        config: Optional[RunnableConfig] = None,
        **kwargs: Any,
    ) -> Any:
        if self._is_tool_call(input):
            tool_call_id: Optional[str] = cast(ToolCall, input)["id"]
            self.tool_call_id = tool_call_id
        return await super().ainvoke(input, config, **kwargs)


    def _run(self, query: str, config: RunnableConfig, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        
        agent_url = os.getenv("AGENT_URL")
        agent_name = os.getenv("AGENT_NAME")

        metadata = TaskMetadata(
            prompt_id = config["metadata"]["thread_id"],
            tool_call_id = self.tool_call_id,
            agent_name = agent_name,
            agent_callback_url = f"http://{agent_url}/task-complete"
        )

        task_attributes = {
            "db_host": self.db_host,
            "db_port" : self.db_port,
            "db_username" : self.db_username,
            "db_password" : self.db_password,
            "db_name" : self.db_name,
            "query": query
        }

        submit_task(self.name, metadata, task_attributes)
        raise NodeInterrupt(f"SQL Query submitted to task server")
    
    def _is_tool_call(self, x: Any) -> bool:
        return isinstance(x, dict) and x.get("type") == "tool_call"
