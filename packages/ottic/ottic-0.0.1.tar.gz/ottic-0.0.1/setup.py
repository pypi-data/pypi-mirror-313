# setup.py
from setuptools import setup, find_packages


setup(
    name='ottic',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='Dmitry Sergeev <dmitry@ottic.ai>',
    author_email='dmitry@ottic.ai',
    description='Ottic AI Python SDK',
)