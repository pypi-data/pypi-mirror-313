# secretvalidate/session_manager.py
import requests

# Disable SSL warnings
requests.packages.urllib3.disable_warnings()

# Create a shared session object
session = requests.Session()

def get_session():
    """Returns the shared requests session."""
    return session

def flus_session():
    """"Removes the Shared request session"""
    session.cache = None
    session.close()