# file: setup.py
# content: setup file for fswp2pdf package
# created: 2025 January 11 Saturday
# modified:
# modification:
# author: roch schanen
# comment:

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fswp2pdf",
    version="0.0.0",
    author="Roch Schanen",
    author_email="r.schanen@lancaster.ac.uk",
    description="frequency sweep data file to pdf file: fit, plot and export.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RochSchanen/fswp2pdf",
    packages = ['fswp2pdf'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['numpy', 'matplotlib', 'scipy'],
    python_requires='>=3.10'
)
