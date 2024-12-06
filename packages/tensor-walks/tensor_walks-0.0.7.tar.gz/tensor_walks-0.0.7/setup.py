#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open("Readme.md", encoding="utf-8") as readme_file:
    readme = readme_file.read()

with open("requirements.txt", encoding="utf-8") as req_file:
    requirements = req_file.read().splitlines()

test_requirements = [
    "pytest>=3",
]

setup(
    author="Johannes Seiffarth",
    author_email="j.seiffarth@fz-juelich.de",
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.8",
    ],
    description="Fast vectorized tree library.",
    install_requires=requirements,
    extras_require={
        "torch": ["torch==2.4.1"],
    },
    license="MIT license",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="tensor_walks",
    name="tensor_walks",
    packages=find_packages(include=["tensor_walks", "tensor_walks.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://jugit.fz-juelich.de/IBG-1/ModSim/tensortree",
    version="0.0.7",
    zip_safe=False,
)
