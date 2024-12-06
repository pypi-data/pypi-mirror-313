from setuptools import setup, find_packages
from typing import List
import os

def get_requirements(file_path: str) -> List[str]:
    """
    Reads the requirements file and returns a list of dependencies.
    """
    try:
        with open(file_path, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Warning: {file_path} not found. Proceeding without additional requirements.")
        return []

long_description = "A comprehensive Python package for automating text preprocessing tasks."
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()

setup(
    name="TPTK",
    version="0.0.7",
    author="Gaurav Jaiswal",
    author_email="jaiswalgaurav863@gmail.com",
    description="Automate text preprocessing tasks with ease.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Gaurav-Jaiswal-1/Text-Preprocessing-Toolkit.git",
    project_urls={
        "Bug Tracker": "https://github.com/Gaurav-Jaiswal-1/Text-Preprocessing-Toolkit/issues",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "pyspellchecker>=0.7.1",
        "spacy>=3.0.0",
        "nltk>=3.6.0",
        "pandas>=1.2.0",
        "matplotlib>=3.3.0"
    ] + get_requirements("requirements.txt"),
    extras_require={
        "dev": [
            "pytest>=7.2.0",
            "pytest-cov>=4.0.0",
            "flake8>=6.0.0",
            "black>=23.1.0",
            "mypy>=0.991",
            "sphinx>=7.1.2",
            "sphinx-rtd-theme>=1.2.0"
        ],
        "nlp": [
            "gensim>=4.0.0"
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Text Processing :: Linguistic"
    ],
    python_requires=">=3.8",
    license="MIT",
    include_package_data=True,
    zip_safe=False
)
