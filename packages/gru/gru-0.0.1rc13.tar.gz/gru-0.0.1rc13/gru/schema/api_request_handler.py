from datetime import datetime
from typing import Dict, Optional
from urllib.parse import urljoin
import requests
from gru.utils.entity_type import EntityType


class APIRequestHandler:
    """
    Handles sending requests to the Yugen remote API.
    """

    def __init__(self, auth_token, config, params = None):
        self.params = params or {}
        self.config = config
        self.base_url = self.config.stuart_api_endpoint
        #TODO: 22-Mar-24    Sandeep Mishra     add authentication header once jwt token implemented accross APIs in Stuart
        self.headers = {
            "Content-type": "application/json",
            "Accept": "text/plain",
            "Authorization": f"Bearer {auth_token}"
        }

    def set_headers(self, headers: dict):
        """
        Updates the request headers with the provided dictionary.
        """
        self.headers.update(headers)
    
    def set_authorization(self, token: str):
        """
        Sets the authorization token in the headers dictionary.

        Args:
            token (str): The authorization (i.e. jwt) token to be set.
        """

        self.headers["Authorization"] = "Bearer {}".format(token)

    def set_params(self, params: dict):
        """
        Sets the request parameters for the next request.
        """
        self.params = params

    def send_request(
        self, method: str, url_path: str, json_data: Optional[dict] = None
    ) -> requests.Response:
        """
        Sends an HTTP request to the Yugen API using the specified method and path.

        Args:
            method (str): The HTTP method (e.g., 'POST', 'GET', 'PATCH', etc.).
            url_path (str): The path relative to the base URL.
            json_data (Optional[dict]): The JSON data to be sent in the request body.

        Returns:
            dict: The response from the API as a dictionary.

        Raises:
            requests.exceptions.RequestException: If there's an issue with the API request.
            ValueError: If a required parameter is missing.
        """

        if not method:
            raise ValueError("Method argument is required")
        if not url_path:
            raise ValueError("url_path argument is required")

        api_url = urljoin(self.base_url, url_path)

        try:
            response = requests.request(
                method=method.upper(), url=api_url, json=json_data, headers=self.headers, params=self.params
            )
            return response
        except requests.exceptions.RequestException as e:
            raise e
    
    def create_register_json(self, register_object) -> Dict:
        """
        Create JSON payload for registration.
        """
        entity_type = register_object.entity_type
        url_path = self.config.register_paths[entity_type]
        return url_path, register_object.to_json()

    def create_deploy_json(self, name: str, entity_type: EntityType,
                            dry_run: Optional[bool]= False, 
                            start_date: Optional[datetime] = None,
                            end_date: Optional[datetime] = None) -> Dict:
        """
        Create JSON payload for deployment.
        """
        url_path =  self.config.deploy_paths[entity_type.value],
        json_req = { "name": name,
                    "type": entity_type.value,
                    "airflow_dags_backup_path": self.config.airflow_dags_backup_path if self.config.airflow_dags_backup_path else None
                }
        
        if dry_run : 
            json_req.update("start_date", start_date)
            json_req.update("end_date", end_date)

        return url_path, json_req
