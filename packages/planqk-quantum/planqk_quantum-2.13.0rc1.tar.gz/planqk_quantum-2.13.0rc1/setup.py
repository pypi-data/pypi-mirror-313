from setuptools import find_namespace_packages, setup

with open("./README.md", "r") as fh:
    long_description = fh.read()

with open("./requirements.txt", "r") as fh:
    requirements = fh.readlines()

setup(
    name="planqk-quantum",
    version="2.13.0-rc1",
    author="Kipu Quantum GmbH",
    author_email="info@kipu-quantum.com",
    url="https://gitlab.com/planqk-foss/planqk-quantum",
    description="Python SDK for the PlanQK Platform",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_namespace_packages(include=["planqk", "planqk.*"]),
    license="apache-2.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    python_requires=">=3.11",
)
