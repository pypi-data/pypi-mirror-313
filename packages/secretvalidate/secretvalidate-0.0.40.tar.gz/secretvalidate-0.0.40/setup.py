from setuptools import setup, find_packages
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), 'secretvalidate', '.env'))

# Retrieve the current version from environment variable
version = os.getenv("VERSION", "0.0.1")

# Get the path to requirements.txt which is one folder up
requirements_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '.', 'requirements.txt'))

# Read requirements from requirements.txt
with open(requirements_path, 'r') as f:
    requirements = f.read().splitlines()

setup(
    name='secretvalidate',
    version=version,
    description='A cli/package for validating secrets.',
    author='VigneshKna',
    author_email='Vkna@email.com',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['*.txt', '../requirements.txt', '../urls.json','.env'],
    },
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'secretvalidate=secretvalidate.validator:main',
        ],
    },
)
