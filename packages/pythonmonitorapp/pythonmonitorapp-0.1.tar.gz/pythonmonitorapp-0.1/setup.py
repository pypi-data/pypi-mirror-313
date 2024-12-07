from setuptools import setup, find_packages
import os

with open("src/requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="pythonmonitorapp",
    version="0.1",
    packages=find_packages(),
    install_requires=required,  # Usa le dipendenze di requirements.txt
)