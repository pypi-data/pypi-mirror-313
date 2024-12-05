"""
To update existing preprocessing transform. Supported values - 
    - "owners"
    - "description"
    - "start_time"
"""
from typing import Dict
from datetime import datetime


class UpdatePreprocessingTransform:
    """
    Update a preprocessing transform 

    Parameters
    ----------
    transform_name: str
        preprocessing transform name to be updated
    property: str
        name of the property to be updated
    new_val: str
        new value for the transform property
    
    Returns
    -------
    None

    Notes
    -----

    Examples
    --------
    >>> obj = UpdatePreprocessingTransform(
    ...         name= 'pre_process_movie_collection',
    ...         property= 'active',
    ...         new_val= False,
    ... )
    ... _
    ... yugen_client.update(update_obj)
    """

    def __init__(self, transform_name, property, new_val):
        self.name = transform_name
        self.property = property
        self.new_val = new_val

        if isinstance(self.new_val, datetime):
            self.new_val = str(self.new_val)


    def to_json(self) -> Dict:
        """
        Convert the UpdateFeature object to a JSON-compatible dictionary.
        """
        return {
            "transform_name": self.name,
            "property": self.property,
            "new_value": self.new_val,
        }