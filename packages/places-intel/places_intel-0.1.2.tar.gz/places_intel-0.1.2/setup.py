from setuptools import setup, find_packages

setup(
    name="places_intel",  # Package name
    version="0.1.2",  # Initial version
    author="Blake Jennings",
    author_email="blake@workerbeetech.com",
    description="A library for fetching and processing place data with polygons using Outscraper and Overpass APIs.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),  # Automatically find sub-packages
    install_requires=[
        "outscraper",
        "overpy",
    ],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)