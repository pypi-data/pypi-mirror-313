"""
To update existing raw and derived features. Supported values - 
    - "owners"
    - "description"
    - "start_time"
    - "online"
    - "offline"
    - "active"
"""

from typing import Dict
from datetime import datetime


class UpdateFeature:
    """
    Update a feature 

    Parameters
    ----------
    feature_name: str
        feature name to be updated
    property: str
        name of the property to be updated
    new_val: str
        new value for the feature property
    
    Returns
    -------
    None

    Notes
    -----

    Examples
    --------
    >>> obj = UpdateFeature(
    ...         name= 'raw_feature_test_v2',
    ...         property= 'active',
    ...         new_val= False,
    ... )
    ... _
    ... yugen_client.update(update_obj)
    """

    def __init__(self, name, property, new_val):
        self.name = name
        self.property = property
        self.new_val = new_val

        if isinstance(self.new_val, datetime):
            self.new_val = str(self.new_val)


    def to_json(self) -> Dict:
        """
        Convert the UpdateFeature object to a JSON-compatible dictionary.
        """
        return {
            "name": self.name,
            "property": self.property,
            "new_value": self.new_val,
        }
