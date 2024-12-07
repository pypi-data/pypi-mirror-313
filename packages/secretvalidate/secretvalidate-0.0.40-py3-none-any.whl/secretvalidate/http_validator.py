# secretvalidate/http_validator.py
import json
import os
import requests

from secretvalidate.env_loader import get_secret_active, get_secret_inactive
from .session_manager import get_session, flus_session

# Use the shared session
session = get_session()

def get_service_url(service):
    """Load service URL from urls.json based on service name."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    urls_path = os.path.join(current_dir, '..', 'urls.json')

    with open(urls_path, 'r') as f:
        urls = json.load(f)

    service_url = urls.get(service)
    if not service_url:
        raise ValueError(f"Error: URL for service {service} not found.")
    return service_url


def get_headers(service, secret):
    """Generate headers based on service type."""
    nocache_headers = {'Cache-Control': 'no-cache'}
    headers_map = {
        'snykkey': {'Authorization': f'token {secret}'},
        'sonarcloud_token': {'Authorization': f'Bearer {secret}'},
        'npm_access_token': {'Authorization': f'Bearer {secret}'},
        'huggingface': {'Authorization': f'Bearer {secret}'},
        'pagerduty_api_key': {'Authorization': f'Token {secret}'},
        'sentry_auth_token': {'Authorization': f'Bearer {secret}'},
        'github_personal_access_token': {'Authorization': f'Bearer {secret}'},
        'openai_api_key': {'Authorization': f'Bearer {secret}'},
        'slack_api_token': {'Authorization': f'Bearer {secret}'},
        'discord_bot_token': {'Authorization': f'Bot {secret}'},
        'launchdarkly_access_token': {'Authorization': f'{secret}' }
    }
    header = headers_map.get(service, {})
    header.update(nocache_headers)  # Updating the no-cache headers to the existing headers
    return header

def validate_http(service, secret, response):
    """Validate HTTP-based services."""
    headers = get_headers(service, secret)
    url = get_service_url(service)

    try:
        with session.get(url, headers=headers, verify=False) as response_data:
            response_data.raise_for_status()  # Raise an HTTPError for bad responses

            if response_data.status_code == 200:
                if response:
                    if service == "sonarcloud_token":
                        return response_data.text
                    return get_secret_active()
                else:
                    try:
                        json_response = response_data.json()
                        return json.dumps(json_response, indent=4)
                    except json.JSONDecodeError:
                        return "Response is not a valid JSON."
            elif response_data.status_code == 429:
                return response_data.text
            else:
                if response:
                    return get_secret_inactive()
                else:
                    return response_data.text
    except requests.HTTPError as e:
        if response:
            return get_secret_inactive()
        else:
            return e.response.text
    except requests.RequestException as e:
        return str(e.response.text)
    # finally:
    #     flus_session()  # Ensure the session is closed after the request
