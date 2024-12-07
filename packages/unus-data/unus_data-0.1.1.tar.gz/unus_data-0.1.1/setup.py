from distutils.core import setup
from setuptools import find_packages

with open('README.rst') as f:
  long_description = f.read()

setup(
  name='unus_data',
  version='0.1.1',
  description='A package to handle protein datacard for the protein project',
  author='Li Minzhang',
  author_email='limzh00@outlook.com',
  long_description=long_description,
  packages=find_packages(),
  license='MIT',
  platforms=['all']
)