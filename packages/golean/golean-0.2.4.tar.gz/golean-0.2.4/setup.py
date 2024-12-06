from setuptools import setup, find_packages
import os

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="golean",
    version="0.2.4",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "requests",
        "python-dotenv",
        "tiktoken"
    ],
    description="A Python package for interacting with the GoLean API service.",
    long_description=long_description,  # Use the content of README.md for PyPI page
    long_description_content_type="text/markdown",  # Ensure it's rendered as Markdown
    author="Connor Peng",
    author_email="jinghong.peng@golean.ai",
    url="https://golean.ai",
    classifiers=[
        "Programming Language :: Python :: 3", 
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires='>=3.6',
    include_package_data=True,
)
