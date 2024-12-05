from typing import Dict
from urllib.parse import urljoin
import requests
from gru.sinks.sink import Sink
from gru.utils.config_reader import ConfigReader
from gru.utils.cloud_providers import CloudProviders
from gru.sinks.sink_family import SinkFamily



class OnlineFeatureStoreReader:
    def __init__(self, key, features, online_fs_servie_url, config_path: str = "./gru/config.yaml", online_feature_store: Sink = None):
        """
        A class representing a feature retrieval service with an online feature store.

        Args:
            key (str): A unique identifier for the feature retrieval request.
            features (list): A list of features to retrieve.
            config_path (str): The path to the configuration file used to initialize the reader.

        Returns:
            OnlineFeatureStoreReader: An instance of the OnlineFeatureStoreReader.

        Example:
            Initialize an OnlineFeatureStoreReader:
            reader = OnlineFeatureStoreReader(key="unique_key", features=["feature1", "feature2"], config_path="/path/to/config.yaml")
        """
        self.key = key
        self.features = features
        self.config = ConfigReader(config_path=config_path)
        if online_feature_store is None:       
            self.validate_config()
            self.online_feature_store = self.config.online_feature_store
        else:
            self.online_feature_store=online_feature_store.to_json()
        self.online_fs_service_url = online_fs_servie_url

    def validate_config(self):
        """
        Validates the family and cloud provider provider by the user in config.yaml
        """
        online_feature_store = self.config.online_feature_store
        try:
            SinkFamily.get_key(online_feature_store["family"])
            CloudProviders.get_key(online_feature_store["cloud_provider"])
        except Exception as e:
            raise e

    def to_json(self) -> Dict: 
        """
        Serialize the OnlineFeatureStoreReader instance to a JSON-compatible dictionary.
        """
        return {
            "key": self.key,
            "features": self.features,
            "online_fs_details": self.online_feature_store,
            "online_fs_service_url": self.online_fs_service_url,
        }

    def get_online_features(self):
        """
        Retrieve feature values for a particular key from an online feature store.

        Sends a GET request to the online feature store service endpoint specified in the configuration
        and retrieves the requested features for the provided key.

        Example:
            Retrieve online features for the initialized OnlineFeatureStoreReader instance:
            reader = OnlineFeatureStoreReader(key="unique_key", features=["feature1", "feature2"], config_path="/path/to/config.yaml")
            reader.get_online_features()
        """
        api_url = urljoin(
                        self.config.stuart_api_endpoint,
                        self.config.online_fs_service_url
        )
        result = requests.get(
            url=api_url,
            json=self.to_json(),
            headers={"Content-type": "application/json", "Accept": "text/plain"},
        )
        print(result.json())
