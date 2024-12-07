
import requests

from secretvalidate.env_loader import get_secret_active, get_secret_inactive
from secretvalidate.session_manager import get_session


# Use the shared session
session = get_session()

def validate_flickr_api(api_key, response):
    """Validate Flickr Api key."""
    url = "https://api.flickr.com/services/rest/"
    params = {
        "method": "flickr.test.echo",
        "api_key": api_key,
        "format": "json",
        "nojsoncallback": "1"
    }

    try:
        response_data = session.get(url, params=params)
        response_data.raise_for_status()  # Raise an HTTPError for bad responses
        response_body = response_data.json()

        if response_data.status_code == 200:
            if "stat" in response_body and response_body["stat"] == "ok":
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
            if response:
                    return get_secret_inactive()
            else:
                return response_body

    except requests.exceptions.RequestException as e:
        if response:
            return get_secret_inactive()
        else:
            return str(e)
