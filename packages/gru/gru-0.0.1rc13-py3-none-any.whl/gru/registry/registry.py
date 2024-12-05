"""
In Machine Leaning, Registry is the store house of all the registered entities. 
Namely:
    - Features
    - Training Data
    - Preprocessing Transforms
    - Data Sources & Data Sinks
"""

import requests

class Registry:
    def __init__(self, access_token):
        self.access_token = access_token

    def get_registered(
            self,
            entity_url: str,
            ) -> list[str]:
        """
        Function to return the list of all entities registered in our platform registry database.
        """

        result = requests.get(
            url=entity_url,
            json={"access_token": self.access_token},
            headers={"Accept": "text/plain", "Content-type": "application/json",},
        )
        return result.json()


    def get_registered_features(self):
        """Function to get the list of all the registered features from the registry database"""
        pass

    def get_registered_data_sources(self):
        """Function to get the list of all the registered data sources from the registry database"""
        pass

    def get_registered_data_sinks(self):
        """Function to get the list of all the registered data sinks from the registry database"""
        pass

    def get_registered_ppt(self):
        """Function to get the list of all the registered Pre Processing Transforms from the registry database"""
        pass

    def get_registered_training_data(self):
        """Function to get the list of all the registered Training Data from the registry database"""
        pass
