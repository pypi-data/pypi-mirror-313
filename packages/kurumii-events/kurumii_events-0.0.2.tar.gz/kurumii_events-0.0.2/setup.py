# setup.py file for the 
from setuptools import setup, find_packages

setup(
    name='kurumii_events',
    version='0.0.2',
    packages=find_packages(),
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'kurumii = kurumii_events.cli:main'
        ]
    }
)