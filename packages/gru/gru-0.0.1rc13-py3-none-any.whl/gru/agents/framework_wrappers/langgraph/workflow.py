import json
import os
from typing import Any

import psycopg
from psycopg_pool import AsyncConnectionPool
from gru.agents.checkpoint.postgres import PostgresAsyncConnectionPool
from gru.agents.framework_wrappers import AgentWorkflow
from langgraph.graph import StateGraph

from gru.agents.schemas import AgentInvokeRequest
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from gru.agents.schemas.schemas import TaskCompleteRequest
from langchain_core.messages import ToolMessage

class LanggraphWorkflow(AgentWorkflow):
    
    def __init__(self, stateGraph: StateGraph) -> None:
        super().__init__()
        self.state_graph = stateGraph

    async def setup(self):
        checkpoint_db_type = os.getenv("CHECKPOINT_DB_TYPE", "postgres")
        if checkpoint_db_type == "postgres":
            pool = PostgresAsyncConnectionPool().get()
            checkpointer = await self._setup_postgres_checkpointer(pool)
            self.compiled_graph = self.state_graph.compile(checkpointer)


    async def invoke(self, request: AgentInvokeRequest) -> dict[str, Any]:
        config = RunnableConfig(
            configurable={"thread_id": request.prompt_id},
        )
        return await self.compiled_graph.ainvoke(input=request.prompt_body, config=config)
    
    async def resume(self, request: TaskCompleteRequest) -> dict[str, Any]:
        config = RunnableConfig(
            configurable={"thread_id": request.prompt_id},
        )
        state = await self.compiled_graph.aget_state(config=config)

        ## todo : Support for Custom state?
        await self.compiled_graph.aupdate_state(
            config=config, 
            values={"messages": [ToolMessage(content=json.dumps(request.result), name=request.task_type, tool_call_id=request.tool_call_id)]}, 
            as_node=state.next[0]
        )

        result = await self.compiled_graph.ainvoke(input=None, config=config)
        return result
    
    async def _setup_postgres_checkpointer(self, pool: AsyncConnectionPool):
        checkpointer = AsyncPostgresSaver(pool)
        async with pool.connection() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute("""
                        SELECT EXISTS (
                            SELECT FROM information_schema.tables 
                            WHERE  table_schema = 'public'
                            AND    table_name   = 'checkpoints'
                        );
                    """)
                    table_exists = (await cur.fetchone())[0]
                    
                    if not table_exists:
                        print("Checkpoints table does not exist. Running setup...")
                        await checkpointer.setup()
                    else:
                        print("Checkpoints table already exists. Skipping setup.")
                except psycopg.Error as e:
                    print(f"Error checking for checkpoints table: {e}")
                    raise e
        return checkpointer
    

    
