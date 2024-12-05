from setuptools import setup, find_packages

setup(
    name="HDDFeat",  
    version="0.1.0",  #
    description="A library for feature selection in high-dimensional datasets",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Said Al Afghani Edsa, Khamron Sunat, P.hD",
    author_email="saidalafghani.dumai@gmail.com",
    url="https://github.com/saiddddd/HDDFeat",  
    packages=find_packages(),
    install_requires=[],  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
