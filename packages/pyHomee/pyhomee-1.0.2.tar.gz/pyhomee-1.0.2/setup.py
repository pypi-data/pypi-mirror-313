import setuptools

__version__ = "1.0.2"

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyHomee",
    version=__version__,
    author="Taraman17",
    description="a python library to interact with homee",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Taraman17/pyHomee",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
