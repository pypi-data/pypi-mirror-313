from setuptools import setup, find_packages

setup(
    name="pyLaysWebhooker",
    version="1.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "pySend = pyLaysWebhooker:pySend",
            "pyInstantSend = pyLaysWebhooker:pyInstantSend"
        ]
    }
)