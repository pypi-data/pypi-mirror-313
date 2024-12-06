from setuptools import setup, find_packages

setup(
    name="aiotica",
    version="1.0.13",
    author="KASO",
    description="Gateway programming library of KASO AioTica",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="",
    package_dir={"": "."},
    packages=find_packages(where="."),
    install_requires=[
        "Rx==3.2.0",
        "paho-mqtt==2.1.0",
        "boto3==1.33.13",
        "awsiotsdk==1.21.4",
        "requests==2.31.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
