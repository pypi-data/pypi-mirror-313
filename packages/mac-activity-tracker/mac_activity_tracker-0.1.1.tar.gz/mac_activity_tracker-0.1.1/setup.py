from setuptools import setup, find_packages
import os

# Read version from _version.py
version_dict = {}
with open('mac_activity_tracker/_version.py', 'r') as f:
    exec(f.read(), version_dict)

setup(
    name="mac-activity-tracker",
    version=version_dict['__version__'],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'mac-activity-tracker=mac_activity_tracker.tracker:main',
        ],
    },
    install_requires=[
        'pynput>=1.7.0',
        'pyobjc-framework-Quartz>=10.0',
        'colorama>=0.4.6',
    ],
)
