# setup.py
from setuptools import setup, find_packages

setup(
    name='lenzf',
    version='0.1',
    description='A custom Python module to calculate the length of various data types',
    author='Yashwant Gokul P',
    author_email='connectwithyg@gmail.com',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
