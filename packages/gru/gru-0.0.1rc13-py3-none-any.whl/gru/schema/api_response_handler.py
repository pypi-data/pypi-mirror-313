import requests
from typing import Union, Optional


class APIResponseHandler:
    """
    Handles responses from the Yugen remote API.

    Attributes:
        response: The raw response from the API.
    """

    def __init__(self, response: requests.Response):
        """
        Initialize the ResponseHandler with a response object.

        Args:
            response: The requests.Response object to handle.
        """
        self.response = response
        self.status_code = self.response.status_code

    def check_for_errors(self):
        """
        Checks if the response contains an error and raises appropriate exceptions.
        """
        response_json = self.response.json()

        if "error" in response_json:
            error = response_json["error"]
            if self.status_code == 500:
                raise InternalServerError(
                    status_code=self.status_code,
                    title="Server Error",
                    message=error["message"],
                )
            elif self.status_code == 400:
                raise BadRequestError(
                    status_code=self.status_code,
                    title="Bad Request",
                    message=error["message"],
                )
            elif self.status_code == 404:
                raise NotFoundError(
                    status_code=self.status_code,
                    title="Entity Not Found",
                    message=error["message"],
                )
            else : 
                raise ApiError(
                    status_code=self.status_code,
                    title=error["title"],
                    message=error["message"],       
                )

            

    def get_success_data(self) -> Optional[Union[dict, list]]:
        """
        Returns the parsed data from a successful response.

        Returns:
            The parsed data if a "data" key is found in the response, otherwise None.
        """
        response_json = self.response.json()
        return response_json.get("data")
    
    def get_message(self) -> str:
        response_json = self.response.json()
        return response_json.get("message")


class ApiError(Exception):
    """
    Represents an error returned by the API.
    """

    def __init__(
        self, status_code: int, title: str, message: str, *args, **kwargs
    ):
        """
        Initializes the ApiError with details from the API response.
        """
        super().__init__(title, message, *args, **kwargs)
        self.status_code = status_code
        self.title = title
        self.message = message

class InternalServerError(ApiError):
    """
    Represents an InternalServerError returned by the API.
    """

    def __init__(
        self, status_code: int, message: str, title: str = "Internal Server Error", *args, **kwargs
    ):
        """
        Initializes the ApiError with details from the API response.
        """
        super().__init__(status_code, title, message,  *args, **kwargs)

class BadRequestError(ApiError):
    """
    Represents a BadRequestError returned by the API.
    """

    def __init__(
        self, status_code: int, message: str, title: str = "Bad Request", *args, **kwargs
    ):
        """
        Initializes the BadRequestError with details from the API response.
        """
        super().__init__(status_code, title, message,  *args, **kwargs)

class NotFoundError(ApiError):

    """
    Represents a NotFoundError returned by the API.
    """

    def __init__(
        self, status_code: int, message: str, title: str = "Entity Not Found", *args, **kwargs
    ):
        """
        Initializes the NotFoundError with details from the API response.
        """
        super().__init__(status_code, title, message,  *args, **kwargs)



