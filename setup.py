from setuptools import setup, find_packages

setup(
    name="chatgpt-assistant",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "python-dotenv",
        "requests",
        "flask",
        "apscheduler",
        "openai",
        "google-api-python-client",
        "beautifulsoup4",
        "pandas",
        "pyyaml",
    ],
    entry_points={
        "console_scripts": [
            "chatgpt-assistant=chatgpt_assistant.main:main",
        ],
    },
)