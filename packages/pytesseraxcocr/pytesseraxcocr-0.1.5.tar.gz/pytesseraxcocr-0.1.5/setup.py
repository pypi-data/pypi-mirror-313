from setuptools import setup, find_packages

setup(
    name='pytesseraxcocr',
    version='0.1.5',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pyzbar'
    ],
    license='MIT',
)