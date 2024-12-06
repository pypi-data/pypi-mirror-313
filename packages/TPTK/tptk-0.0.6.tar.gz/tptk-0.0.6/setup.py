from setuptools import setup, find_packages
from typing import List
import os

# Constant for editable install
HYPHEN_E_DOT = "-e ."

def get_requirements(file_path: str) -> List[str]:
    """
    Reads the requirements file and returns a list of dependencies.
    Removes the editable install option if present.
    """
    requirements = []
    try:
        with open(file_path, "r") as f:
            requirements = f.readlines()
            # Strip newlines and remove editable install if it exists
            requirements = [req.strip() for req in requirements if req.strip()]
            if HYPHEN_E_DOT in requirements:
                requirements.remove(HYPHEN_E_DOT)
    except FileNotFoundError:
        print(f"Warning: {file_path} not found. Proceeding with empty requirements.")
    return requirements

# Read the long description from README.md or use a fallback
long_description = (
    "A comprehensive Python package for automating text preprocessing tasks "
    "such as tokenization, lemmatization, stopword removal, and normalization."
)
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()

# Define primary dependencies
dependencies = [
    "pyspellchecker>=0.7.1",
    "spacy>=3.0.0",
    "nltk>=3.6.0",
    "pandas>=1.2.0",
    "matplotlib>=3.3.0",
]

# Package metadata
setup(
    name="TPTK",  # Package name
    version="0.0.6",  # Incremented version for updates
    author="Gaurav Jaiswal",
    author_email="jaiswalgaurav863@gmail.com",
    description="Automate text preprocessing tasks with ease using TPTK.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Gaurav-Jaiswal-1/Text-Preprocessing-Toolkit.git",
    project_urls={
        "Bug Tracker": "https://github.com/Gaurav-Jaiswal-1/Text-Preprocessing-Toolkit/issues",
        "Source Code": "https://github.com/Gaurav-Jaiswal-1/Text-Preprocessing-Toolkit",
    },
    package_dir={"": "src"},  # Source code lives in the `src` directory
    packages=find_packages(where="src"),  # Automatically discover all packages
    install_requires=dependencies + get_requirements("requirements.txt"),  # Add dependencies
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
    ],
    keywords=[
        "text preprocessing",
        "NLP",
        "natural language processing",
        "tokenization",
        "lemmatization",
        "text cleaning",
        "TPTK",
    ],
    python_requires=">=3.8",  # Specify minimum Python version
    extras_require={
        "dev": [  # Developer dependencies
            "pytest>=7.2.0",
            "pytest-cov>=4.0.0",
            "flake8>=6.0.0",
            "black>=23.1.0",
            "mypy>=0.991",
            "sphinx>=7.1.2",
            "sphinx-rtd-theme>=1.2.0",
        ],
        "nlp": dependencies + [  # NLP-specific tools
            "gensim>=4.0.0",
        ],
    },
    include_package_data=True,  # Include additional files specified in MANIFEST.in
    license="MIT",  # License type
    zip_safe=False,  # Ensure package is safe to run zipped
)
