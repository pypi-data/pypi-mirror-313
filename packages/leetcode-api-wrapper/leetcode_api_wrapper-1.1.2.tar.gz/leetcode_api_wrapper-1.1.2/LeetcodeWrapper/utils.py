from urllib.parse import urlencode
from .exceptions import ValidationError


def build_url(base_url, endpoint, params=None):
    """Builds a complete URL with optional query parameters.

    Args:
        base_url (str): The base URL of the API.
        endpoint (str): The API endpoint.
        params (dict, optional): Query parameters to append to the URL.

    Returns:
        str: The complete URL.
    """
    url = f"{base_url}{endpoint}"
    if params:
        query_string = urlencode(params)
        url = f"{url}?{query_string}"
    return url


def validate_username(username):
    """Validates the username input.

    Args:
        username (str): The username to validate.

    Raises:
        ValidationError: If the username is empty or not a string.
    """
    if not username or not isinstance(username, str):
        raise ValidationError("Username must be a non-empty string")
