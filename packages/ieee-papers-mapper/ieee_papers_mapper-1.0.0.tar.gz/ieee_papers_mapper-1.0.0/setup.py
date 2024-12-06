#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name="ieee_papers_mapper",
    version="1.0.0",
    author="Alexandros Anastasiou",
    author_email="anastasioyaa@gmail.com",
    description="A project for fetching, processing, and classifying IEEE papers.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/alex-anast/ieee-papers-mapper",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.12",
    # List only the parent packages needed, not their dependencies as well
    # It is not the same as `requirements.txt` !!!
    install_requires=[
        "dash",
        "pandas",
        "dotenv",
        "python-dotenv",
        "transformers",
        "torch",
        "torchvision",
        "torchaudio",
        "sympy",
        "pillow",
        "networkx",
        "mpmath",
        "APScheduler",
    ],
)
