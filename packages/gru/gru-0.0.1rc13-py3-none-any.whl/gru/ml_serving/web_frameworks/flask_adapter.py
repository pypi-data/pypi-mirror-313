"""
    Adapter for the Flask web framework.

    This class extends the WebFrameworkAdapter and provides concrete implementations for the abstract methods.

    Methods:
        - __init__: Initialize the FlaskAdapter instance.
        - predict: Implementing the method for making predictions in Flask.
        - process_request: Implementing the method for processing requests in Flask.
        - format_response: Implementing the method for formatting responses in Flask.
        - load_model: Implementing the method for loading user BYOC code in Flask.
        - load_assets: Implementing the method to load assets in Flask.
        - start_server: Implementing the method to start the Flask server and spin up the inference endpoint.
"""

import importlib
from gru.ml_serving.ml_serving_config_reader import MLServingConfigReader
from gru.ml_serving.request_handler import RequestHandler
from gru.ml_serving.response_handler import ResponseHandler
from .web_framework_adapter import WebFrameworkAdapter

class FlaskAdapter(WebFrameworkAdapter):

    def __init__(self, config: MLServingConfigReader):
        """
        Initialize the FlaskAdapter instance.

        Parameters:
            - config: MLServingConfigReader instance for reading configuration settings.
        """
        super().__init__(config)

    def predict(self, input_data):
        """
        Make predictions in Flask.

        Parameters:
            - input_data: Input data for making predictions.

        Returns:
            Any: Predicted results in Flask.
        """
        pass

    def process_request(self, request):
        """
        Process incoming requests in Flask.

        Parameters:
            - request: Request object received from the Flask web framework.

        Returns:
            dict: Processed request data in Flask.
        """
        return RequestHandler.parse_request(request)

    def format_response(self, response):
        """
        Format and send responses in Flask.

        Parameters:
            - response_data: Data to be included in the response.

        Returns:
            Any: Formatted response in Flask.
        """
        return ResponseHandler.format_response(response)

    def load_application(self):
        """
        Load user BYOC code in Flask.

        Returns:
            Any: Loaded user code in Flask.
        """
        try:
            spec = importlib.util.spec_from_file_location("flask_app", self.config.get_config('entrypoint'))

            if spec is None:
                raise Exception(f"Error importing file: {self.config.get_config('entrypoint')}")
            
            app_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(app_module)
            return app_module.application
        
        except Exception as e:
            raise Exception(f"Error loading flask application: {str(e)}")
        
