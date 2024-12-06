from setuptools import setup, find_packages

setup(
    name="xlitellm",
    version="0.1.0",
    description="A client library for making requests to various LLMs through a unified interface",
    author="Sam Meng",
    packages=find_packages(),
    install_requires=[
        "litellm==1.52.8",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)
