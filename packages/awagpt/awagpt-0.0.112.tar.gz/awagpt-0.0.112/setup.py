from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="awagpt",
    version="0.0.112",
    description="AwaGPT is a powerful Python library designed by Awarri Technologies for developers to interact with advanced localalized language and audio models that have been trained with local Nigerian data.",
    packages=find_packages(),  # Automatically discover the `awagpt` package
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Awarri/awagpt",
    author="Awarri",
    author_email="moses@awarri.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests >= 2.32.3"],
    python_requires=">=3.8.10",
)
