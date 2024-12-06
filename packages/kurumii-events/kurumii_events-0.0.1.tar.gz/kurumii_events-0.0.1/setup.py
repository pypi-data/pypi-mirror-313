# setup.py file for the 
from setuptools import setup, find_packages

setup(
    name='kurumii-events',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'kurumii = kurumii_events.cli:main'
        ]
    }
)
