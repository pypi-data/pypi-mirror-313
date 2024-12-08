class ApiError(Exception):
    """
    Exception raised for errors returned by the API.
    """

class AcledMissingAuthError(ValueError):
    pass
