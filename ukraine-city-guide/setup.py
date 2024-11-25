from setuptools import setup, find_packages

setup(
    name="ukraine-city-guide",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'customtkinter>=5.2.0',
        'rdflib>=6.3.2',
        'tkintermapview',
        'pytest',
        'pytest-cov'
    ]
)