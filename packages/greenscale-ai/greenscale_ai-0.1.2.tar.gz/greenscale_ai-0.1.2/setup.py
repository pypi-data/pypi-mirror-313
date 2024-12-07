from setuptools import setup, find_packages

setup(
    name="greenscale-ai",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
    ],
    author="Greenscale AI",
    author_email="hello@greenscale.ai",
    description="Python SDK for Greenscale AI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/greenscale-ai/greenscale-ai-sdk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)