from setuptools import setup, find_packages

setup(
    name="HighdimensionalFeat",  
    version="0.1.1",  #
    description="A library for feature selection in high-dimensional datasets",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Said Al Afghani Edsa, Khamron Sunat, P.hD",
    author_email="saidalafghani.dumai@gmail.com",
    url="https://github.com/saiddddd/HighdimensionalFeat",  
    packages=find_packages(),
    install_requires=[],  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
