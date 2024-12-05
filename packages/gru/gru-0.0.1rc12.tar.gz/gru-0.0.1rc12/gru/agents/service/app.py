from contextlib import asynccontextmanager
from fastapi import BackgroundTasks, FastAPI, Response
import uvicorn
from gru.agents.framework_wrappers import AgentWorkflow
from gru.agents.schemas import AgentInvokeRequest, AgentInvokeResponse
from gru.agents.schemas.schemas import TaskCompleteRequest

@asynccontextmanager
async def lifespan(app: FastAPI):

    workflow: AgentWorkflow = app.state.workflow
    await workflow.setup()
    yield
        
api = FastAPI(lifespan=lifespan)

async def invoke_workflow(request: AgentInvokeRequest):
    workflow: AgentWorkflow = api.state.workflow
    output = await workflow.invoke(request)
    # Todo: Save output to DB table
    print(output)

async def resume_workflow(request: TaskCompleteRequest):
    workflow: AgentWorkflow = api.state.workflow
    output = await workflow.resume(request)
    # Todo: Save output to DB table
    print(output)

@api.post("/invoke")
async def invoke(request: AgentInvokeRequest, background_tasks: BackgroundTasks) -> AgentInvokeResponse:
    background_tasks.add_task(invoke_workflow, request)
    return AgentInvokeResponse(prompt_id=request.prompt_id)

@api.post("/task-complete")
async def task_complete(request: TaskCompleteRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(resume_workflow, request)
    return Response(status_code=200)

class App:

    def __init__(self, workflow: AgentWorkflow):
        api.state.workflow = workflow

    def run(self):
        uvicorn.run(api, host="0.0.0.0", port=8080)