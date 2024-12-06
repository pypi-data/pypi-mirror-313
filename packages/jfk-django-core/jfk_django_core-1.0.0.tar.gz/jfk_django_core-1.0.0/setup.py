from setuptools import setup
from setuptools_scm import get_version

setup(
    version=get_version(),
    setup_requires=['setuptools_scm'],
)