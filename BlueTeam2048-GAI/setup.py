from setuptools import setup, find_packages
import os


setup(
    name='blue2048',
    version='0.1',
    description='Blue 2048',
    classifiers=['Programming Language :: Python'],
    packages=find_packages(),
    include_package_data=True,
    package_data = {
      'iccp.api.tests': data_files,
    },
    install_requires=[
        'Keras',
        'Theano',
    ],
)
