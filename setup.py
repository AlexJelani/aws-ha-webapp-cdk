from setuptools import setup, find_packages
setup(
    name="high_availability_app",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "aws-cdk-lib",
        "constructs",
    ],
)
