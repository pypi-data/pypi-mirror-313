from setuptools import setup, find_packages

setup(
    name="palcodeinfra",
    version="0.1.6",
    packages=find_packages(),
    install_requires=[
        "sqlalchemy",
        "pydantic",
        "pydantic-settings",
        "psycopg",
        "boto3",
        "pyyaml"
    ],
    python_requires=">=3.12",
    author="Palcode",
    author_email="palcode@palcode.ai",
    description="A package containing infrastructure functionalities to build apis",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Palcode-ai/palcode-infrastructure",
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)