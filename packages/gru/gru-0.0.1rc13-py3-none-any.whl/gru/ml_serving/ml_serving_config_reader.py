"""
Server Configuration Reader

This module provides a class, MLServingConfigReader, for reading and accessing
configuration settings from a YAML file.

Usage:
    - Instantiate MLServingConfigReader with the path to the configuration YAML file.
    - Use the provided methods to access specific configuration settings.
"""
import yaml

class MLServingConfigReader:

    def __init__(self, config_file_path):
        """
        Initialize the MLServingConfigReader instance.

        Parameters:
            - config_file_path: Path to the configuration YAML file.
        """
        self.config_file_path = config_file_path
        self.read_config()

    def read_config(self):
        """
        Read and load the configuration settings from the YAML file.
        """
        with open(self.config_file_path, 'r') as file:
            self.config = yaml.safe_load(file)

        config_validator = MLServingConfigValidator(self.config)
        config_validator.validate_config()

    def get_config(self, key):
        """
        Get the value of a specific configuration setting by key.

        Parameters:
            - key: Key for the configuration setting.

        Returns:
            Any: Value of the specified configuration setting.
        """
        return self.config.get(key)


class MLServingConfigValidator:
    """
    Configuration validator for ML serving.

    Methods:
        - __init__: Initialize the MLServingConfigValidator instance with a configuration dictionary.
        - validate_config: Validate the configuration dictionary for required keys.
        - validate_webserver_config: Validate the 'webserver' configuration for required keys.
    """

    def __init__(self, config):
        """
        Initialize the MLServingConfigValidator instance.

        Parameters:
            - config: Configuration dictionary.
        """
        self.config = config

    def validate_config(self):
        """
        Validate the configuration dictionary for required keys.
        """
        required_keys = ['ml_project', 'ml_service_name', 'serving_layer', 'entrypoint', 'webserver']
        self.check_required_key(required_keys, self.config)
            
        supported_keys = ['ml_project', 'ml_service_name', 'serving_layer', 'entrypoint', 'webserver', 'env_vars', 'models', 'artifacts']
        self.check_supported_key(supported_keys, self.config)

        self.validate_webserver_config()

    def validate_webserver_config(self):
        """
        Validate the 'webserver' configuration for required keys.
        """
        webserver_config = self.config.get('webserver')

        required_keys = ['type', 'config']
        self.check_required_key(required_keys, webserver_config)
            
        supported_keys = ['type', 'config']
        self.check_supported_key(supported_keys, webserver_config)
            
    def check_required_key(self, required_keys, config: dict):
        """
        Check if all required keys are present in the configuration.

        Raises:
            ValueError: If any required key is missing in the configuration.
        """
        for key in required_keys:
            if key not in config:
                raise ValueError(f"Missing required key: {key} in config yaml")
    
    def check_supported_key(self, supported_keys, config):
        """
        Check if all keys in the configuration are supported.

        Raises:
            ValueError: If any key in the configuration is not supported.
        """
        for key in config:
            if key not in supported_keys:
                raise ValueError(f"Unsupported key: {key} in config yaml")
