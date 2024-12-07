
import requests
from requests.auth import HTTPBasicAuth

from secretvalidate.env_loader import get_secret_active, get_secret_inactive
from secretvalidate.session_manager import get_session


# Use the shared session
session = get_session()

def verify_secret_format(secret, separator=":"):
    """
    Checks if the string contains the separator ":".
    
    :param string: The input string to check.
    :param separator: The separator to look for (default is ':').
    :return: True if the separator is found, False otherwise.
    """
    return separator in secret

def split_username(string, separator=":"):
    """
    Splits the string into two variables using the separator ":".
    
    :param string: The input string to split.
    :param separator: The separator to use for splitting (default is ':').
    :return: A tuple containing the two parts of the string.
    """
    return string.split(separator)

def validate_browserstack(secret, response):
    """Validate Browserstack Api key."""
    url = "https://www.browserstack.com/automate/plan.json"
    
    try:
        if verify_secret_format(secret):
            user, api_key = split_username(secret)
            auth = HTTPBasicAuth(user, api_key)

            response_data = session.get(url, auth=auth)
            response_data.raise_for_status()  # Raise an HTTPError for bad responses
            response_body = response_data.json()

            if response_data.status_code == 200:
                if response:
                    return get_secret_active()
                else:
                    return response_body
            else:
                if response:
                        return get_secret_inactive()
                else:
                    return response_body
        else:
            return "Browserstack secret format to be in 'USERNAME:API_KEY'"

    except requests.exceptions.RequestException as e:
        if response:
            return get_secret_inactive()
        else:
            return str(e)
