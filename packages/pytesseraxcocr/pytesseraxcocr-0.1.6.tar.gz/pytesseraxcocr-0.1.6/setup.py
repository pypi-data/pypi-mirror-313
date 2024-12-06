from setuptools import setup, find_packages

setup(
    name='pytesseraxcocr',
    version='0.1.6',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pyzbar'
    ],
    license='MIT',
)