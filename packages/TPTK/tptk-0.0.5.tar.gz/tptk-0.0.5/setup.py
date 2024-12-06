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

# Read the long description from the README.md file or use a fallback description
long_description = "A powerful toolkit for automating text preprocessing tasks."
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()

# Package metadata
setup(
    name="TPTK",  # Package name
    version="0.0.5",  # Initial version
    author="Gaurav Jaiswal",  # Author's name
    author_email="jaiswalgaurav863@gmail.com",  # Author's email
    description=(
        "A Python package for automating text preprocessing tasks like "
        "tokenization, lemmatization, stop word removal, and normalization."
    ),  # Short description
    long_description=long_description,  # Long description from README.md
    long_description_content_type="text/markdown",  # Content type for PyPI
    url="https://github.com/Gaurav-Jaiswal-1/Text-Preprocessing-Toolkit.git",  # Repository URL
    project_urls={  # Additional project links
        "Bug Tracker": "https://github.com/Gaurav-Jaiswal-1/Text-Preprocessing-Toolkit/issues",
        "Documentation": "https://github.com/Gaurav-Jaiswal-1/Text-Preprocessing-Toolkit/wiki",
    },
    package_dir={"": "src"},  # Source code is in the `src` directory
    packages=find_packages(where="src"),  # Automatically find packages in `src`
    install_requires=get_requirements("requirements.txt"),  # Install dependencies
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Text Processing :: Linguistic",
    ],
    keywords=["text preprocessing", "NLP toolkit", "text processing"],  # Keywords
    python_requires=">=3.8",  # Minimum Python version
    extras_require={  # Optional development dependencies
        "dev": [
            "pytest>=7.2.0",
            "pytest-cov>=4.0.0",
            "flake8>=6.0.0",
            "black>=23.1.0",
            "mypy>=0.991",
            "sphinx>=7.1.2",
            "sphinx-rtd-theme>=1.2.0",
        ]
    },
    include_package_data=True,  # Include additional files like README.md
)
