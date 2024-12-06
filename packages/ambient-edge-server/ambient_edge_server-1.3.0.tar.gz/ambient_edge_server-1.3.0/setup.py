# setup.py
from setuptools import setup, find_packages

PACKAGE_NAME = 'ambient_edge_server'
VERSION = '1.3.0'
DESCRIPTION = 'Ambient Edge Server'

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=open('README.md').read(),
    packages=find_packages(),
    install_requires=open('requirements.txt').read().splitlines(),
    entry_points={
        'console_scripts': [
            'ambient_edge_server=ambient_edge_server.run:run',
        ],
    },
    author='Ambient Labs Computing - An Edge Compute Company',
    author_email='jose@ambientlabscomputing.com',
    package_data={'ambient_edge_server': ['templates/*.jinja2', 'assets/*.txt', 'builtin_plugins.yml']},
)
