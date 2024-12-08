
from setuptools import setup, find_packages

setup(
    name="currency_converter_lite",
    version="0.1.0",
    description="A Library for currency conversion in Real Time",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Ameer Adeigbe",
    author_email="ameeradeigbe@gmail.com",
    url="https://github.com/AmeerTechsoft/currency-converter",
    packages=find_packages(),
    install_requires=[ 
        "yfinance",
        "requests",
        "beautifulsoup4",],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)