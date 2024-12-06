"""Setup for ml-management package."""
from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

with open("VERSION", encoding="utf-8") as f:
    version = f.read()

setup(
    name="ml-management",
    version=version,
    description="Python implementation of model pattern, dataset",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="ISPRAS MODIS",
    author_email="modis@ispras.ru",
    maintainer="Maxim Ryndin",
    packages=find_packages(include=["ML_management", "ML_management.*"]),
    include_package_data=True,
    install_requires=[
        "sgqlc==16.1",
        "boto3==1.34.70",
        "aioboto3==13.1.1",
        "jsonschema==4.18.4",
        "tqdm==4.66.6",
        "pydantic>=1,<2",
        "jsf==0.7.1",  # update when TDM will support pydantic>=2.0.0
        "pylint>=3,<4",
        "httpx<1",
        "websocket-client==1.6.1",
        "pandas==2.0.3",
        "PyYAML==6.0.1",
        "numpy==1.26.4",
        "matplotlib==3.7.2",
    ],
    package_data={
        "": ["*.yaml"],
    },
    data_files=[("", ["VERSION"])],
    python_requires=">=3.8",
)
