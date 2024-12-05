from setuptools import setup, find_packages

setup(
    name="ploppie",
    version="0.3.0",
    packages=find_packages(),
    install_requires=[
        "litellm",
        "pillow",
    ],
    author="Ben Baptist",
    author_email="me@benbaptist.com",
    license=open("LICENSE.md").read(),
    description="A high-level, stupid-simple Pythonic LiteLLM abstraction layer for implementing simple chat workflows, with tools.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/benbaptist/pyploppie",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
