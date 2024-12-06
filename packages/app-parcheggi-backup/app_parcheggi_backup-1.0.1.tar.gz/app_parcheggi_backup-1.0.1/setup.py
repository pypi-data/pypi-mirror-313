from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name='app-parcheggi-backup',
    version='1.0.1',
    description='Progetto Python per la gestione dei parcheggi',
    packages=find_packages(),
    install_requires=requirements,
)