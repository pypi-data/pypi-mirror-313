from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="xlitellm",
    version="0.1.1",
    description="A client library for making requests to various LLMs through a unified interface",
    long_description=long_description,
    long_description_content_type='text/markdown',
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
