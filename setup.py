from setuptools import setup, find_packages

setup(
    name='nasstat',
    version='0.1.0',
    author='Dariel Cruz Rodriguez',
    author_email='hello@dariel.us',
    description='A python wrapper of the United States Federal Aviation Authority National Airspace System API developed by Dariel Cruz Rodriguez.',
    packages=find_packages(),
    install_requires=["requests",],
    classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)