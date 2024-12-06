from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name='auto-parcheggi-backup',
    version='1.0',
    description='Progetto Python per la gestione dei parcheggi',
    packages=find_packages(),
    install_requires=requirements,
)