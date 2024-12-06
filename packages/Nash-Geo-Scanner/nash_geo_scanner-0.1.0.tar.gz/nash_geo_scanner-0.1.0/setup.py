from setuptools import setup, find_packages

setup(
    name="Nash-Geo-Scanner",  # Unique package name on PyPI
    version="0.1.0",  # Initial version
    author="Mohammed Althaf",
    author_email="althafnash14@gmail.com",
    description="Geo locator",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Althafnash/Nash-NetGeoScanner-.git",
    packages=find_packages(),  # Automatically find and include packages
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum Python version
    install_requires=[],  # List of dependencies
)
