from setuptools import setup, find_packages

setup(
    name="toolkit_ds",
    version="0.1.0",
    author="Aravind S",
    author_email="aravind@inbo.tech",
    description="A Python package implementing core data structures and algorithms.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ARAVIND281/ds_toolkit",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
