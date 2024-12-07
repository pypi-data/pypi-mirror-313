from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='libdom',
    version='0.0.1',
    #url='https://github.com/caiocarneloz/pacotepypi',
    license='MIT License',
    author='Pedro Salles',
    long_description=readme,
    long_description_content_type="text/markdown",
    #author_email='',
    keywords='Html, Builder, Html Builder',
    description=u'Html Builder',
    packages=['libdom'],)