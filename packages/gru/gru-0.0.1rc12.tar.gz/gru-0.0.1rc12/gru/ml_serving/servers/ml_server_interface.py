"""
ML Server Interface.

This abstract base class defines the interface for a machine learning server.

Methods:
    - start: Abstract method to start the server.
    - stop: Abstract method to stop the server.
    - reload: Abstract method to reload the server.
    - load: Abstract method to load the server.
"""

from abc import ABC, abstractmethod

class MLServerInterface(ABC):

    @abstractmethod
    def start(self):
        """Abstract method to start the server."""
        pass

    @abstractmethod
    def stop(self):
        """Abstract method to stop the server."""
        pass

    @abstractmethod
    def reload(self):
        """Abstract method to reload the server."""
        pass

    @abstractmethod
    def load(self):
        """Abstract method to load the server."""
        pass

