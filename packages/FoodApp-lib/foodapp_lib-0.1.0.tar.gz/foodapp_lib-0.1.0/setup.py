# setup.py
from setuptools import setup, find_packages

setup(
    name='FoodApp_lib',
    version='0.1.0',
    description='A library for managing food orders and employees in a Django application.',
    author='Aakash',
    author_email='aakashbabu75399@gmail.com',
    packages=find_packages(),
    install_requires=[
        'django>=3.0',
        'boto3',


    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
    ],
)
