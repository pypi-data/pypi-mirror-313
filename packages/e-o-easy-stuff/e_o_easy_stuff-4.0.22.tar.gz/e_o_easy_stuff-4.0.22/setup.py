from setuptools import setup, find_packages
import codecs
import os

VERSION = '4.0.22'
DESCRIPTION = 'Easy tools'
LONG_DESCRIPTION = 'Easy tools'

# Setting up
setup(
    name="e-o-easy_stuff",
    version=VERSION,
    author="Gideon",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pyspark'],
    keywords=['pyspark'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
