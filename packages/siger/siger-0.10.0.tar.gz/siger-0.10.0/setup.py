# pip install git+https://<token>@github.com/nkbueno/siger.git
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    description = f.read()

setup(
    name='siger',
    version='0.10.0',
    description='Automações em Python para auxiliar obtenção de dados do SIGER-CEPEL',
    author='Nathan Kelvi de Almeida Bueno',
    author_email='nathankelvi@gmail.com',
    url='https://github.com/nkbueno/siger',
    packages=['siger'],
    install_requires=[
        'pandas',
        'numpy',
        'requests',
        'beautifulsoup4',
        'selenium',
        'DateTime',
        'pywin32',
        'xlsxwriter',
    ],
    long_description=description,
    long_description_content_type="text/markdown",
)
