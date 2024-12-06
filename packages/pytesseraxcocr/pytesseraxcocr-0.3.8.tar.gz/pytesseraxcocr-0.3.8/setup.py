from setuptools import setup, find_packages

setup(
    name='pytesseraxcocr',
    version='0.3.8',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pyzbar',
        'Pillow'
    ],
    license='MIT',
)