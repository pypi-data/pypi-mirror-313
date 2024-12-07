from setuptools import find_packages
from setuptools import setup

setup(
    name="cdbt",
    version="0.4.10",
    description="A CLI tool to manage dbt builds with state handling and manifest management",
    author="Craig Lathrop",
    author_email="development@coldborecapital.com",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0,<9.0.0",
        "pyperclip>=1.8.0,<2.0.0",
        "snowflake-connector-python[pandas]>=3.11.0,<4.0.0",
        "python-dotenv>=1.0.0,<1.2.0",
        "openai>=1.35.0,<2.0.0",
        "sqlfluff==3.2.5",
        "sqlfluff-templater-dbt==3.2.5",
        "wordninja==2.0.0",
        "ruamel.yaml<0.18.0",
    ],
    entry_points={
        "console_scripts": [
            "cdbt=cdbt.cmdline:cdbt",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
