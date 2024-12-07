import subprocess
import sys

from secretvalidate.env_loader import get_packagename
from secretvalidate.session_manager import get_session

# Use the shared session
session = get_session()

# Custom type function to convert input to lowercase
def lowercase_choice(value):
    return value.lower()

def format_services(services):
    """Format service choices as a bullet-point list."""
    return "\n".join([f"  - {service}" for service in services])

def update_tool():
    """Update the tool to the latest version."""
    # Use 'pip3' for Python 3.x and 'pip' for Python 2.x or if Python 3.x is the default interpreter
    pip_command = "pip3" if sys.version_info.major == 3 else "pip"
    try:
        subprocess.run([pip_command, "install", "--upgrade",
                       f"{get_packagename()}"], check=True)
        print("Tool updated to the latest version.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to update the tool: {e}")


def get_version():
    url = f"https://pypi.org/pypi/{get_packagename()}/json"
    response = session.get(url)

    if response.status_code == 200:
        data = response.json()
        return data['info']['version']
    else:
        return None