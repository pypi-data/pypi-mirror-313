import requests
import time
import logging

from epx.config import read_auth_config

logger = logging.getLogger(__name__)


def retry_request(method, url, headers=None, params=None, data=None, json=None):
    """
    Makes an HTTP request with retries and exponential backoff.

    Args:
        method (str): HTTP method to use ('GET', 'POST', etc.).
        url (str): The endpoint URL.
        headers (dict): Headers for the HTTP request.
        params (dict): Query parameters for GET requests.
        data (dict): Form data for POST requests.
        json (dict): JSON payload for POST requests.
        max_retries (int): Maximum number of retry attempts.
        backoff_factor (int): Factor by which the sleep time is increased.

    Returns:
        requests.Response: The HTTP response object.

    Raises:
        ConnectionError
            If all retries fail.
    """

    try:
        max_retries = read_auth_config("max-retries")
    except Exception:
        max_retries = 3  # default value

    max_retries = check_positive_integer(max_retries, "max-retries")

    try:
        backoff_factor = read_auth_config("backoff-factor")
    except Exception:
        backoff_factor = 2  # default value

    backoff_factor = check_positive_integer(backoff_factor, "backoff-factor")

    for attempt in range(max_retries):
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                data=data,
                json=json,
            )
            return response
        except requests.exceptions.ConnectionError as e:
            if attempt < max_retries - 1:
                sleep_time = backoff_factor**attempt
                logger.error(
                    f"Connection reset error: {e} "
                    + f"--- Retrying in {sleep_time} seconds..."
                )
                time.sleep(sleep_time)
            else:
                logger.error("All retries FAILED:" + f" Connection reset error: {e}")
                raise e


def check_positive_integer(value, attribute_name):
    if not isinstance(value, int) or value <= 0:
        raise ValueError(
            f"'{attribute_name}' must be a positive integer, but got {value}."
        )
    return value
