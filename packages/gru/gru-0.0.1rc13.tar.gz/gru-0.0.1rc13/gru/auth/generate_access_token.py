"""
Create access token and update access token for client authentication.
"""
from typing import Dict


class GenerateAccessToken:
    def __init__(
        self,
        client_id,
        user_email,
        password,
    ):
        self.client_id = client_id
        self.user_email = user_email
        self.password = password

    def to_json(self) -> Dict:
        """
        Represent generate token Object
        Parameters:
        ----------
        client_id (str):
            client id for user.
        user_email (str):
            user email of user.
        password (str):
            password of user.
        """
        return {
            "client_id": self.client_id,
            "user_email": self.user_email,
            "password": self.password,
        }
