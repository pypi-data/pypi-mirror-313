from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="zimra",
    version="0.0.2",
    packages=find_packages(),
    description="Unofficial Python wrapper for the ZIMRA FDMS API by Tarmica Chiwara",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Tarmica Chiwara",
    author_email="tarimicac@gmail.com",
    url="https://github.com/lordskyzw/zimra",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
