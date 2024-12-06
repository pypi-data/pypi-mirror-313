""" Setup version from git Tag for the package. """
import os
from setuptools import setup


setup(
    version=os.environ.get('BUILD_VERSION', '0.0.0'),
)
