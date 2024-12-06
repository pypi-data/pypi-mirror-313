#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

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
    description="An open-source Python package, t_office_365 providing easy-to-use classes and methods for \
    interacting with Microsoft Office 365 services, including SharePoint, OneDrive, Outlook, and Excel, with features \
    such as file management, email handling, and spreadsheet operations.",
    long_description=readme,
    keywords="t_office_365",
    name="t_office_365",
    packages=find_packages(include=["t_office_365", "t_office_365.*"]),
    test_suite="tests",
    url="https://www.thoughtful.ai/",
    version="0.1.23",
    zip_safe=False,
    install_requires=install_requirements,
)
