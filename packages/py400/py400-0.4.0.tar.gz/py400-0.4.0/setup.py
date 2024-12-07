from setuptools import setup, find_packages

setup(
    name='py400',
    version='0.4.0',
    description='A library to facilitate interactions with IBM i hosts using python.',
    authors = [
        { "name" : "Nathanaël Renaud", "email" : "nathanael.renaud@hutchinson.com" },
    ],
    packages=find_packages(include=["py400"]),
    install_requires=["itoolkit>=1.7.2", "pyodbc>=5.1.0"]
)