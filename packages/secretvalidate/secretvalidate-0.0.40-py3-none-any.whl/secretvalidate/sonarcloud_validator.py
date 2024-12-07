#secretvalidate/sonarqube_validator.py
import json

from secretvalidate.http_validator import validate_http
from secretvalidate.env_loader import get_secret_active, get_secret_inactive

def validate_sonarcloud(secret, response):
    res = json.loads(validate_http("sonarcloud_token", secret, response)).get("settings")
    for item in res:
        if "onboarding.dismiss" in item.get("key"):
            return get_secret_inactive()
    return get_secret_active()
