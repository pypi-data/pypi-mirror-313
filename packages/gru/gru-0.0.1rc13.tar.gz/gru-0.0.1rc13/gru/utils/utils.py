"""
Utils Module consists of all helper functions and classes
"""


def check_data_type(field_datatypes_dict: dict) -> bool:
    """
    To ensure that the datatype of the value passed by the end user is correct

    Parameters
    ----------
    field_datatypes_dict:
        dict with datatypes as keys and value is the list of fields accepted as that datatype

    Returns
    -------
    bool:
        True, if encountered a field with incorrect datatype
        False, if all fields are of correct datatype

    Notes
    -----
    Even though the function returns None, still it prints success/failure message

    Examples
    --------
    """
    args_type_check = True
    for data_type, fields in field_datatypes_dict.items():
        for field in fields:
            if not isinstance(field, data_type):
                print(str(field), f"is supposed to be {data_type}")
                args_type_check = False
                return args_type_check

    return args_type_check


class Constants:
    """
    Constants Class to declare all the constant values that will be used across all modules
    """

    # Stuart API
    STUART_API_ENDPOINT = "http://35.154.143.223/"  # prod API endpoint

    # Infra
    API_DEPLOY_INFRA_DEV = STUART_API_ENDPOINT + "deploy/infrastructure"
    API_DEPLOY_INFRA_PROD = STUART_API_ENDPOINT + "deploy/infrastructure"

    # Infra
    REGISTER_INFRA_URL = STUART_API_ENDPOINT + "register/infrastructure"

    # Generate Training Data
    GTD_STAGE = "dev"
    GTD_JOB_TIMEOUT = 30
    GTD_REQUEST_ID = "01"
    GTD_REQUEST_TYPE = "gtd"
    TRAINING_DATA = "TRAINING_DATA"
    GTD_K8S_NAMESPACE = "airflow-jobs"
    GTD_REGISTER_URL = STUART_API_ENDPOINT + "training_data/register"
    GTD_GENERATE_DATA_URL = STUART_API_ENDPOINT + "training_data/generate"

    AIRFLOW_DAGS_BACKUP_PATH = "s3://internal-ml-demos/dags/"

    def __init__(self) -> None:
        pass