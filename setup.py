from setuptools import setup, find_namespace_packages


setup(
    name="weatherapp.rp5",
    version="0.1.0",
    author="Vasyl Rostykus",
    description="Rp5Weather provider",
    long_description="",
    packages=find_namespace_packages(),
    entry_points={
        'weatherapp.provider': 'rp5=weatherapp.rp5.provider:Rp5Provider',
    },
    install_requires=[
        'requests',
        'bs4',
    ],
)
