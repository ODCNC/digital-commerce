from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="digital-commerce",
    version="0.0.1",
    author="David Jeong",
    author_email="hyjeong@odcnc.co.kr",
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
    install_requires=requirements,
)
