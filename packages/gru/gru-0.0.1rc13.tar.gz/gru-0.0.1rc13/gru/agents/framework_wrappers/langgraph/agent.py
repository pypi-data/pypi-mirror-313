from gru.agents.framework_wrappers import BaseAgent
from langgraph.graph import StateGraph

from gru.agents.framework_wrappers.langgraph.workflow import LanggraphWorkflow
from gru.agents.service.app import App

class CansoLanggraphAgent(BaseAgent):

    def __init__(self, stateGraph: StateGraph) -> None:
        workflow = LanggraphWorkflow(stateGraph)
        self.app = App(workflow)

    def run(self):
        self.app.run()

