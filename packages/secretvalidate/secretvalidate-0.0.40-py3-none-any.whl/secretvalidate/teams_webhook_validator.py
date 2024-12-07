
import requests

from secretvalidate.env_loader import get_secret_active, get_secret_inactive
from secretvalidate.session_manager import get_session
import json


# Use the shared session
session = get_session()

def validate_teams_webhook(webhook_url, response):
    """Validate Teams webhook URL."""
    payload = {'text': 'test message'}
    headers = {'Content-Type': 'application/json'}

    try:
        response_data = requests.post(webhook_url, headers=headers, data=json.dumps(payload))
        response_body = response_data.text

         # Check for error message in response body even if status code is 200
        if response_data.status_code == 200:
            if "Microsoft Teams endpoint returned HTTP error 404" in response_body:
                # Handle case where 404 error is in the response message
                if response:
                    return get_secret_inactive()
                else:
                    return f"Teams webhook error detected in response body: {response_body}"
            else:
                # No error detected; consider it a successful validation
                return get_secret_active() if response else "Teams webhook URL validation successful!"

        if response_data.status_code == 400:
            if 'Text is required' in response_body:
                if response:
                    return get_secret_active()
                else:
                    return "Teams webhook URL validation successful!"
            else:
                if response:
                    return get_secret_inactive()
                else:
                    return f"Unexpected response body: {response_body}"
        elif response_data.status_code < 200 or response_data.status_code >= 500:
            if response:
                return get_secret_inactive()
            else:
                return f"Unexpected HTTP response status: {response_data.status_code}"
        else:
            if response:
                return get_secret_inactive()
            else:
                return "Unexpected error"
    except requests.exceptions.RequestException as e:
        if response:
            return get_secret_inactive()
        else:
            return str(e)
