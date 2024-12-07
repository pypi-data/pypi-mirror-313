<p align="center">
  <h2 align="center">SecretValidate</h2>
  <p align="center">Validate leaked credentials.</p>
</p>

---

# :mag_right: Now Validating

- Browserstack_auth_url
- Discord_bot_token
- Flickr_api_key
- Github_personal_access_token
- Huggingface
- Mongodb
- Npm_access_token
- Openai_api_key
- Pagerduty_api_key
- Sentry_auth_token
- Slack_api_token
- Snykkey
- Sonarcloud_token
- Teams_webhook

# :tv: SecretValidate Demo

https://github.com/user-attachments/assets/24b7c699-fc78-4e57-a40a-94164d768ae6

```python
secretvalidate -service <<SECRET_TYPE>> -secret <<YOUR_SECRET>> -r
```

# :floppy_disk: Installation

Several options available for you:

### Python package

```bash
pip install secretvalidate
```

### NPM package - (Yet to be Published)

```bash
npm i secretvalidate
```

# :memo: Usage

Secretvalidate has a below secret types for validating:

- Browserstack_auth_url
- Discord_bot_token
- Flickr_api_key
- Github_personal_access_token
- Huggingface
- Mongodb (Beta)
- Npm_access_token
- Openai_api_key
- Pagerduty_api_key
- Sentry_auth_token
- Slack_api_token
- Snykkey
- Sonarcloud_token
- Teams_webhook

See the `-h` or `--help` flag for usage and details:

```
$ secretvalidate -h
Secret Validator Tool
Use this tool to validate various types of secrets for different services.

options:
  -h, --help            show this help message and exit
  -service              Service / SecretType to validate secrets.
                        Supported services:
                          - snykkey
                          - sonarcloud_token
                          - npm_access_token
                          - huggingface
                          - pagerduty_api_key
                          - sentry_auth_token
                          - mongodb
                          - teams_webhook
                          - github_personal_access_token
                          - openai_api_key
                          - slack_api_token
                          - discord_bot_token
                          - flickr_api_key
                          - browserstack_auth_url
  -secret SECRET        Pass Secrets to be validated
  -r, --response        Prints Active/ InActive upon validating secrets.
  -v, --version         Show the version of this tool and exit.
  --update              Update the tool to the latest version.
```

## Validation Example (Python)

```python
from secretvalidate.validator import validate

"""
Validate the secret key for the specified service.
Args:
    service (str): The service name.
    secret (str): The secret key.
    response (bool): The response Active/Inactive
Returns:
    str: The validation result.
"""
try:
    result = validate(service, secret, response=True/False)
    return result
except Exception as e:
    return f"Error: {e}"
```
