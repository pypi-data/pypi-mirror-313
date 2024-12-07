# setup.py

from setuptools import setup, find_packages

setup(
    name='api_gerenciador',
    version='0.20.0',
    description='Biblioteca que executa ações de uma API',
    author='Rafael Gomes de Oliveira',
    author_email='rafaelprotest4@gmail.com',
    packages=find_packages(),
    install_requires=[
        'python-dotenv'
    ],
)
