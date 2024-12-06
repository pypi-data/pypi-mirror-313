#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

install_requirements = open("requirements.txt").readlines()

setup(
    author="Thoughtful",
    author_email="support@thoughtful.ai",
    python_requires=">=3.9",
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    description="t-desktop is a Python library that provides common methods for desktop automation, simplifying"
    "tasks like window management, keyboard, and mouse control.",
    long_description_content_type="text/markdown",
    long_description=readme,
    keywords="t_desktop",
    name="t_desktop",
    packages=find_packages(include=["t_desktop", "t_desktop.*"]),
    test_suite="tests",
    url="https://www.thoughtful.ai/",
    version="0.0.14",
    zip_safe=False,
    install_requires=install_requirements,
    include_package_data=True,
)
