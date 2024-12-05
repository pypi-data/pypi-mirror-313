from setuptools import setup, find_packages

VERSION = '0.0.5' 
DESCRIPTION = 'The MADCUBA python package.'

# Setting up
setup(
    name="madcubapy", 
    version=VERSION,
    author="David Haasler García",
    author_email="dhaasler@cab.inta-csic.es",
    description=DESCRIPTION,
    long_description=open('README.rst', 'r').read(),
    long_description_content_type='text/x-rst',
    url='https://github.com/dhaasler/madcubapy',
    packages=find_packages(),
    install_requires=[
        "astropy>=7.0.0",
        "matplotlib>=3.9.0",
        "numpy>=1.26.0"
    ],
    keywords=[
        'madcuba',
        'radio astronomy',
    ],
    classifiers= [
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
