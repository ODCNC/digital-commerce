from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="digital-commerce",
    author="David Jeong",
    description="A common package for digital commerce.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ODCNC/digital-commerce",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
