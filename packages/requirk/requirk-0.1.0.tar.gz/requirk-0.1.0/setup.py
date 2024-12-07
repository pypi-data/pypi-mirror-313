from setuptools import find_packages, setup

setup(
    name='requirk',
    packages=find_packages(include=['requirk']),
    version='0.1.0',
    description='A verry good library for dependencies handeling',
    author='robert19066',
    install_requires=[],
    setup_requires=['pytest-runner'],
    test_suite=''
)