"""
Abstract base class for web framework adapters.

This class defines a set of methods that act as a bridge between the generic server and the specific features of a web framework. 
It provides a framework for making predictions, processing requests, formatting and sending responses, loading user BYOC (Bring Your Own Code) code, and managing assets and server startup.

Methods:
    - __init__: Initialize the WebFrameworkAdapter instance with a configuration reader.
    - predict: Abstract method for making predictions.
    - process_request: Abstract method for processing incoming requests.
    - format_response: Abstract method for formatting and sending responses.
    - load_application: Abstract method for loading user BYOC code.
"""

from abc import ABC, abstractmethod
from gru.ml_serving.ml_serving_config_reader import MLServingConfigReader

class WebFrameworkAdapter(ABC):

    def __init__(self, config: MLServingConfigReader):
        """
        Initialize the WebFrameworkAdapter instance with a configuration reader.

        Parameters:
            - config: MLServingConfigReader instance for reading configuration settings.
        """
        self.config = config

    @abstractmethod
    def predict(self, input_data):
        """
        Make predictions based on input data.

        Parameters:
            - input_data: Input data for making predictions.

        Returns:
            Any: Predicted results.
        """
        pass

    @abstractmethod
    def process_request(self, request):
        """
        Process incoming requests.

        Parameters:
            - request: Request object received from the web framework.

        Returns:
            dict: Processed request data.
        """
        pass

    @abstractmethod
    def format_response(self, response_data):
        """
        Format and send responses.

        Parameters:
            - response_data: Data to be included in the response.

        Returns:
            Any: Formatted response.
        """
        pass

    @abstractmethod
    def load_application(self, code_path):
        """
        Load user BYOC (Bring Your Own Code) from the specified path.

        Parameters:
            - code_path: Path to the user code.

        Returns:
            Any: Loaded user code.
        """
        pass
