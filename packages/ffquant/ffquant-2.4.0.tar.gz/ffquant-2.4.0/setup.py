from setuptools import setup, find_packages

setup(
    name="ffquant",
    version="2.4.0",
    description="A python package for providing fintech indicators",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Jonathan Lee",
    author_email="lihuapinghust@gmail.com",
    url="https://github.com/lihuapinghust/ffquant",
    packages=find_packages(),
    install_requires=[
        "backtrader==1.9.78.123",
        "matplotlib==3.9.2",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
