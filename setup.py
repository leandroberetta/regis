from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='regis',
    version='0.0.1',
    description='Docker Registry (API v2) UI',
    long_description=readme,
    author='Leandro Beretta',
    author_email='lea.beretta@gmail.com',
    license=license,
    packages=find_packages(exclude=('tests'))
)