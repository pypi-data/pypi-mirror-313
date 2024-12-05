"""
The `YugenClient` class serves as a client for registering, deploying, and simulating objects using a remote API.
It provides functionalities to interact with a backend system to manage various types of feature objects.
"""

from datetime import datetime
import json
import os
from typing import Optional, Type, Union, Dict
import requests
from gru.agents.apis import AGENT_CONFIG_FILE_NAME, deploy_agent, prompt_agent, read_prompt_file, register_agent
from gru.features.update_feature import UpdateFeature
from gru.ai_agents.agent_deployment import AIAgent
from gru.ai_agents.send_rabbitmq_message import AIAgentMessage
from gru.preprocess.update_preprocessing_transform import UpdatePreprocessingTransform
from gru.schema.api_request_handler import APIRequestHandler
from gru.schema.api_response_handler import APIResponseHandler, ApiError
from gru.schema.registrable import Registrable
from gru.utils.config_reader import ConfigReader
from urllib.parse import urljoin
from gru.utils.deployment_workflow import Workflow, get_deployment_request_class
from gru.utils.entity_type import EntityType
from gru.auth.generate_access_token import GenerateAccessToken
from gru.components.apis import setup as component_setup


import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class YugenClient:
    """
    A client for registering objects with a remote API.

    Attributes:
        access_token (str): The access token for authentication.
        config (ConfigReader): An instance of the configuration reader.
    """

    def __init__(
        self, auth_token: Optional[str] = None, config_path="./gru/config.yaml"
    ):
        """
        Initialize the YugenClient.

        Args:
            access_token (str): The access token for authentication.
            config_path (str): The path to the configuration file.

        Raises:
            FileNotFoundError: If the specified configuration file does not exist.
        """
        if auth_token is None:
            auth_token = os.environ.get("AUTH_TOKEN")
        if auth_token is None:
            raise KeyError(
                "The auth_token client option must be set either by passing auth token to the client or by setting the AUTH_TOKEN environment variable"
            )
        self.auth_token = auth_token
        try:
            self.config = ConfigReader(config_path=config_path)
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found: '{config_path}'")
        self.request_handler = APIRequestHandler(
            auth_token=self.auth_token, config=self.config
        )
        self.headers = {
            "Content-type": "application/json",
            "Accept": "text/plain",
            "access-token": self.auth_token,
        }

    def register(self, register_object: Registrable) -> dict:
        """
        Register an object with the remote API.

        Args:
            register_object: The object to register.

        Returns:
            dict: The response from the API.

        Raises:
            ValueError: If the given object type cannot be registered.
            requests.exceptions.RequestException: If there's an issue with the API request.

        This function registers an object with the remote API based on its type.
        The function checks the type of the register_object and sends the appropriate API request to register it.

        Example usage:
        >>> from gru.sources.datasource import DataSource
        >>> data_source = DataSource(name="example_source", ... )  # Create a DataSource object
        >>> yugen_client.register(data_source)  # Register the DataSource
        """

        if isinstance(register_object, Registrable):
            try:

                url_path, json_req = self.request_handler.create_register_json(
                    register_object=register_object
                )

                response = self.request_handler.send_request(
                    method="post", url_path=url_path, json_data=json_req
                )

                response_handler = APIResponseHandler(response)
                response_handler.check_for_errors()

                data = response_handler.get_success_data()
                print(data)

            except requests.exceptions.RequestException as e:
                print(f"Connection error: {e}")
            except ApiError as e:
                print(f"API error: {e.title} - {e.message}")
        else:
            raise TypeError(
                f"The provided object of type `{register_object.entity_type}` is not Registrable"
            )

    def deploy(
        self,
        name: str,
        entity_type: EntityType,
        workflow: Workflow = Workflow.AIRFLOW,
        dry_run: Optional[bool] = False,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> dict:
        """
        Deploy an object with the remote API.

        Args:
            entity (Any): The deployable entity.
            deployment_strategy (DeploymentStrategy, optional): The deployment strategy to use. Defaults to None.
            name (Optional[str], optional): Name for the deployment. Defaults to None.
            dry_run (Optional[bool], optional): Whether to perform a dry run. Defaults to False.
            start_date (Optional[datetime], optional): Deployment start date. Defaults to None.
            end_date (Optional[datetime], optional): Deployment end date. Defaults to None.

        Returns:
            dict: The response from the API.
        """

        deployment_request_type = get_deployment_request_class(workflow)
        deployment_strategy_instance = deployment_request_type(
            workflow_name=name,
            entity_type=entity_type,
            config=self.config,
            dry_run=dry_run,
            start_date=start_date,
            end_date=end_date,
        )

        if deployment_strategy_instance.is_entity_deployable():
            deployment_options = (
                deployment_strategy_instance.create_deployment_options()
            )
            url_path = deployment_options.get("url_path")
            json_req = deployment_options.get("json")

            try:
                response = self.request_handler.send_request(
                    method="post", url_path=url_path, json_data=json_req
                )

                response_handler = APIResponseHandler(response)
                response_handler.check_for_errors()

                data = response_handler.get_success_data()
                print(data)

            except requests.exceptions.RequestException as e:
                print(f"Connection error: {e}")
            except ApiError as e:
                print(f"API error: {e.title} - {e.message}")
        else:
            raise TypeError(
                f"The provided entity type `{entity_type}` is not Depoyable with {workflow.value}"
            )

    def update(
        self,
        update_obj: Union[Type[UpdateFeature], Type[UpdatePreprocessingTransform]],
        entity_type: EntityType,
    ):
        """
        Update an existing object of a specific entity type through the remote API.

        Args:
            update_obj (Union[Type[UpdateFeature], Type[UpdatePreprocessingTransform]]):
                The object representing the updates to be made.
            entity_type (EntityType):
                The type of entity to update. It should be one of the supported EntityType values.

        Returns:
            dict:
                The response from the API containing the results of the update.

        This method allows updating an existing object of a specific entity type through the remote API.
        It checks if the provided entity type is valid for updates and sends the appropriate API request
        to update the object.

        Example usage:
        >>> from gru.features.update_feature import UpdateFeature
        >>> update_feature = UpdateFeature(name="updated_feature", ...)  # Create an UpdateFeature object
        >>> yugen_client.update(update_feature, EntityType.RAW_FEATURE)  # Update the Raw Feature object.
        """
        for type in self.config.update_types:
            if entity_type.value == type:
                try:
                    url_path_id = str(
                        self.config.update_paths[type].replace("{id}", update_obj.name)
                    )
                    print(url_path_id)
                    api_url = urljoin(self.config.stuart_api_endpoint, url_path_id)

                    json_req = update_obj.to_json()

                    json_req["type"] = type
                    json_req[
                        "airflow_dags_backup_path"
                    ] = self.config.airflow_dags_backup_path
                    response = requests.patch(
                        url=api_url,
                        json=json_req,
                        headers=self.headers,
                    )

                    response.raise_for_status()
                    print(response.json())
                    return response.json()
                except requests.exceptions.RequestException as e:
                    raise e
                except Exception:
                    raise ValueError(f"Failed to update the object. ")

        raise ValueError(f"The given object type cannot be updated. ")

    def generate_token(self, generate_token_object: GenerateAccessToken):
        """
        Perform create user and generate access token for users.
        Args:
            generate_token_obj: The object to generate token.

        Returns:
            dict: The response from the API.
        """
        try:
            api_url = urljoin(
                self.config.stuart_api_endpoint,
                self.config.generate_token,
            )
            json_req = generate_token_object.to_json()

            response = requests.post(url=api_url, json=json_req, headers=self.headers)

            response.raise_for_status()
            print(response.json())
            return response.json()
        except requests.exceptions.RequestException as e:
            raise e
        except Exception:
            raise ValueError(
                f"Failed to register user and create access token for: '{generate_token_object.user_email}'."
            )

    def get_feature_health(
        self,
        entity_type: EntityType = EntityType.RAW_FEATURE,
        feature_name: Optional[str] = None,
    ) -> dict:
        """
        Retrieve the health status of a feature.

        Args:
            feature_name (str, optional): The name of the feature. If provided, retrieves the health
                status of the specific feature. If not provided, retrieves the overall health status
                of all features.

        Returns:
            dict: The response from the API.

        Raises:
            requests.exceptions.RequestException: If there's an issue with the API request.
            ValueError: If the feature name is provided but invalid.

        Example usage:
        >>> yugen_client.get_feature_health()  # Retrieve overall health status of all features
        >>> yugen_client.get_feature_health("feature-name1")  # Retrieve health status of a specific feature
        """
        try:
            if entity_type.value in self.config.health_types:
                url_path = self.config.health_paths[entity_type.value]
                if feature_name:
                    url_path = f"{url_path}/{feature_name}"
                response = self.request_handler.send_request(
                    method="GET", url_path=url_path
                )

                if response.status_code == 200:
                    logger.info(f"response: {response.json()}")
                    return response.json()
                else:
                    logger.warning(
                        f"Failed to retrieve feature health: {response.json()}"
                    )
                    return {}
            else:
                raise ValueError("Health data not supported for the given entity type")
        except Exception as e:
            logger.error(f"Failed to retrive feature health: {str(e)}")
            return {}

    def deploy_ai_agent(self, ai_agent: AIAgent) -> Dict:
        """
        Deploy an AI agent with the remote API.

        Args:
            ai_agent (AIAgent): The AIAgent object to deploy.

        Returns:
            dict: The response from the API.

        Raises:
            requests.exceptions.RequestException: If there's an issue with the API request.
            ValueError: If the deployment fails.
        """
        try:
            url_path = self.config.api_endpoints["ai_agent"]["deploy"]
            json_req = ai_agent.to_json()

            response = self.request_handler.send_request(
                method="post", url_path=url_path, json_data=json_req
            )

            response_handler = APIResponseHandler(response)
            response_handler.check_for_errors()

            return response_handler.get_success_data()

        except requests.exceptions.RequestException as e:
            raise ValueError(f"Network error during AI agent deployment: {str(e)}")
        except ApiError as e:
            raise ValueError(f"Failed to deploy AI agent: {e.message}")

    def send_rabbitmq_data(self, ai_agent_name: str, message: AIAgentMessage) -> Dict:
        """
        Send a message to an AI agent.

        Args:
            ai_agent_name (str): The name of the AI agent to send the message to.
            message (AIAgentMessage): The message to send to the AI agent.

        Returns:
            dict: The response from the API.

        Raises:
            requests.exceptions.RequestException: If there's an issue with the API request.
            ValueError: If sending the message fails.
        """
        try:
            url_path = self.config.api_endpoints["ai_agent"]["send_message"]
            json_req = {"ai_agent_name": ai_agent_name, "message": message.to_json()}

            response = self.request_handler.send_request(
                method="post", url_path=url_path, json_data=json_req
            )

            response_handler = APIResponseHandler(response)
            response_handler.check_for_errors()

            return response_handler.get_success_data()

        except requests.exceptions.RequestException as e:
            raise ValueError(
                f"Network error during send message to rabbit MQ: {str(e)}"
            )
        except ApiError as e:
            raise ValueError(f"Failed to send message to rabbit MQ: {e.message}")
    
    def setup_component(self, cluster_name:str, config_file:str):
        try:
            return component_setup(cluster_name, config_file, self.auth_token)
        except FileNotFoundError:
            raise ValueError(f"Error: {config_file} file not found.")
        except ApiError as api_error:
            raise ValueError(api_error.message)
        
    def register_agent(self, agent_folder, cluster_name, image, image_pull_secret):
        try:
            return register_agent(self.auth_token, agent_folder, cluster_name, image, image_pull_secret)
        except FileNotFoundError:
            raise ValueError(f"Error: {os.path.join(agent_folder, AGENT_CONFIG_FILE_NAME)} file not found.")
        except ApiError as api_error:
            raise ValueError(api_error.message)
    
    def deploy_agent(self, agent_name):
        try:
           return deploy_agent(self.auth_token, agent_name)
        except ApiError as api_error:
            raise ValueError(api_error.message)
    
    def prompt_agent(self, agent_name: str, prompt_file: str):
        try:
            prompt_data = read_prompt_file(prompt_file)
            return prompt_agent(agent_name, prompt_data, self.auth_token)
        except FileNotFoundError as e:
            raise ValueError(f"File error: {str(e)}")
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON error: {str(e)}")
