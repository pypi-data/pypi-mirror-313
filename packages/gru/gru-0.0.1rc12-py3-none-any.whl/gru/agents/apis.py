import json
import os
import yaml

from gru import DEFAULT_CANSO_API_CONFIG
from gru.agents.models import AgentPromptRequest, AgentRegisterRequest
from gru.schema.api_request_handler import APIRequestHandler
from gru.schema.api_response_handler import APIResponseHandler
from gru.utils.config_reader import ConfigReader

from cookiecutter.main import cookiecutter

AGENT_CONFIG_FILE_NAME = "config.yaml"

AI_AGENT_TEMPLATE_URL = "git@github.com:Yugen-ai/canso-ai-agent-templates.git"

def ai_agent_templates_setup():
    """
    Run Cookiecutter with the specified template.
    """
    cookiecutter(AI_AGENT_TEMPLATE_URL, checkout="agent-template-changes")

def register_agent(auth_token, agent_folder, cluster_name, image, image_pull_secret):
    
    config_file_path = os.path.join(agent_folder, AGENT_CONFIG_FILE_NAME)

    with open(config_file_path, "r") as config_file:
            config_dict = yaml.safe_load(config_file)
    
    agent_register_request = AgentRegisterRequest(
          cluster_name=cluster_name,
          agent_name=config_dict["agent_name"],
          image=image,
          image_pull_secret=image_pull_secret,
          task_server_name=config_dict["task_server_name"],
          checkpoint_db_name=config_dict["checkpoint_db_name"],
          replicas=config_dict["replicas"]
    )

    request_json = agent_register_request.model_dump()

    configs = ConfigReader(DEFAULT_CANSO_API_CONFIG)
    request_handler = APIRequestHandler(auth_token, configs)
    response = request_handler.send_request("post", configs.agent_register_endpoint, request_json)
    response_handler = APIResponseHandler(response)
    response_handler.check_for_errors()

    return response_handler.get_message()

def deploy_agent(auth_token, agent_name):

    configs = ConfigReader(DEFAULT_CANSO_API_CONFIG)
    request_handler = APIRequestHandler(auth_token, configs)
    url = configs.agent_deploy_endpoint.replace("{agent_name}", agent_name)
    response = request_handler.send_request("post", url)
    response_handler = APIResponseHandler(response)
    response_handler.check_for_errors()

    return response_handler.get_message()

def prompt_agent(agent_name: str, prompt: dict, auth_token: str):
    """
    Send a prompt to a deployed agent.
    
    Args:
        agent_name (str): Name of the deployed agent
        prompt (dict): Dictionary containing the prompt data
        auth_token (str): Authentication token for API access
    
    Returns:
        AgentPromptResponse: Response containing the prompt ID
        
    Raises:
        ApiError: If the API request fails
        ValueError: If the request parameters are invalid
    """
    prompt_request = AgentPromptRequest(prompt=prompt)
    request_json = prompt_request.model_dump()
    
    configs = ConfigReader(DEFAULT_CANSO_API_CONFIG)
    request_handler = APIRequestHandler(auth_token, configs)
    
    endpoint = configs.agent_prompt_endpoint.replace("{agent_name}", agent_name)
    
    response = request_handler.send_request("post", endpoint, request_json)
    response_handler = APIResponseHandler(response)
    response_handler.check_for_errors()
    
    response_data = response_handler.get_success_data()
    return response_data

def read_prompt_file(prompt_file: str) -> dict:
    """
    Read and parse a JSON prompt file.
    
    Args:
        prompt_file (str): Path to the JSON file containing prompt data
        
    Returns:
        dict: Parsed prompt data
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    try:
        with open(prompt_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Prompt file not found: {prompt_file}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"Invalid JSON in {prompt_file}: {str(e)}", 
            e.doc, 
            e.pos
        )

