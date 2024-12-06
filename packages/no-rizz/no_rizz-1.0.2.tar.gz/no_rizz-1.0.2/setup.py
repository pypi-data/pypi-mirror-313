from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'readme.md'), encoding='utf-8') as f:
    readme_text = f.read()

setup(
    name="no_rizz",
    version="1.0.2",
    packages=find_packages(),
    install_requires=[
        "google-auth-oauthlib>=1.2.1",
        "google-api-python-client>=2.154.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    long_description=readme_text,  # Add the README content here
    long_description_content_type='text/markdown',
)
