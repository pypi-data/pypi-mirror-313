from enum import Enum

class DataProcessingParadigm(Enum):
    """
    Enum class representing various programming paradigms.
    """

    Batch = "batch"
    Streaming = "streaming"


    @classmethod
    def get_key(cls, value: str) -> 'DataProcessingParadigm':
        """
        Get the enum value for a given string representation.

        Args:
            paradigm_str (str): A string representing a programming paradigm.

        Returns:
            Paradigms: The corresponding enum value if found, or None if not found.
        """
        for paradigm in cls:
            if paradigm.value == value:
                return paradigm
        raise ValueError(f"No matching enum for value: {value}")