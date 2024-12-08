from setuptools import setup, find_packages

setup(
    name="TPTK",
    version="0.0.8",
    author="Gaurav Jaiswal",
    author_email="jaiswalgaurav863@gmail.com",
    description="Automate text preprocessing tasks with ease.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Gaurav-Jaiswal-1/Text-Preprocessing-Toolkit",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "nltk>=3.6.0",
        "pyspellchecker>=0.7.1",
        "pandas>=1.2.0",
    ],
    python_requires=">=3.8",
)
