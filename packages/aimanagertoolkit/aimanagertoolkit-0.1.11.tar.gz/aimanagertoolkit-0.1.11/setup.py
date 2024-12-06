from setuptools import setup, find_packages
from aimanagertoolkit import __version__
from pathlib import Path

with Path("requirements.txt").open() as f:
    install_requires = f.read().splitlines()

setup(
    name="aimanagertoolkit", 
    version=__version__,
    author="Gustavo Inostroza",
    author_email="gusinostrozar@gmail.com",
    description="A toolkit for working with OpenAI and Azure OpenAI API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Inostroza-Wingsoft/AiManagerToolkit",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=install_requires,
)