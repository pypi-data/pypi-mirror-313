import os
from typing import Any
from celery import Celery
from pydantic import BaseModel

broker = os.getenv("BROKER_URL")

task_server = Celery('task_server', broker=broker)

class TaskMetadata(BaseModel):
    prompt_id: str
    tool_call_id: str
    agent_name: str
    agent_callback_url: str

def submit_task(task_type: str, metadata: TaskMetadata, task_attributes: dict[str, Any]):
    task_metadata = metadata.model_dump()
    task_server.send_task("src.tasks.execute", args=[task_type, task_metadata, task_attributes])