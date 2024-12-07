from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    description = f.read()
setup(
    name="pyLaysWebhooker",
    version="1.3",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "pySend = pyLaysWebhooker:pySend",
            "pyInstantSend = pyLaysWebhooker:pyInstantSend"
        ]
    },
    long_description=description,
    long_description_content_type='text/markdown'
)