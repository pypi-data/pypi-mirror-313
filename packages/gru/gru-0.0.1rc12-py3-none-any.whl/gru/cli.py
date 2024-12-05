import os
import fire
import subprocess
import json

from gru.agents.apis import AGENT_CONFIG_FILE_NAME, ai_agent_templates_setup, deploy_agent, read_prompt_file, register_agent
from gru.agents.apis import prompt_agent
from gru.components.apis import setup as component_setup
from gru.schema.api_response_handler import ApiError
from gru.utils.constants import TOKEN_ENV_VAR_NAME

def read_token() -> str:
    auth_token = os.getenv(TOKEN_ENV_VAR_NAME)
    if auth_token == None:
        raise ValueError(f"Environment variable {TOKEN_ENV_VAR_NAME} missing")
    return auth_token


class ComponentCommands(object):
    def setup(self, cluster_name: str, config_file: str):
        try:
            auth_token = read_token()
            result = component_setup(cluster_name, config_file, auth_token)
            return str(result)
        except FileNotFoundError:
            return f"Error: {config_file} file not found."
        except ApiError as api_error:
            return api_error.message
        except ValueError as value_error:
            return str(value_error)


class AgentCommands(object):
    def create_bootstrap(self):
        try:
            ai_agent_templates_setup()
            return f"Agent bootstrap project created successfully!"
        except subprocess.CalledProcessError as value_error:
            return str(value_error)
        
    def register(self, agent_folder, cluster_name, image, image_pull_secret):
        try:
           auth_token = read_token()
           result = register_agent(auth_token, agent_folder, cluster_name, image, image_pull_secret)
           return str(result)
        except FileNotFoundError:
            return f"Error: {os.path.join(agent_folder, AGENT_CONFIG_FILE_NAME)} file not found."
        except ApiError as api_error:
            return api_error.message
        except ValueError as value_error:
            return str(value_error)
    
    def deploy(self, agent_name):
        try:
           auth_token = read_token()
           result = deploy_agent(auth_token, agent_name)
           return str(result)
        except ApiError as api_error:
            return api_error.message
        except ValueError as value_error:
            return str(value_error)
            
    def prompt(self, agent_name: str, prompt_file: str) -> str:
        """
        Send a prompt to a deployed agent.
        
        Args:
            agent_name (str): Name of the deployed agent
            prompt_file (str): Path to JSON file containing the prompt
            
        Returns:
            str: Success or error message
        """
        try:
            auth_token = read_token()
            prompt_data = read_prompt_file(prompt_file)
            result = prompt_agent(agent_name, prompt_data, auth_token)
            return str(result)
        except FileNotFoundError as e:
            return f"File error: {str(e)}"
        except json.JSONDecodeError as e:
            return f"JSON error: {str(e)}"
        except ApiError as e:
            return f"API error: {e.message}"
        except ValueError as e:
            return f"Value error: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"

class GruCommands(object):
    def __init__(self):
        self.component = ComponentCommands()
        self.agent = AgentCommands()


def main():
    fire.Fire(GruCommands)
