from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='libdom',
    version='0.0.2',
    #url='https://github.com/caiocarneloz/pacotepypi',
    license='MIT License',
    author='Pedro Salles',
    long_description=readme,
    long_description_content_type="text/markdown",
    #author_email='',
    keywords='Html, Builder, Html Builder',
    description=u'LibDOM is a Python library that abstracts all modern HTML tags, enabling you to build dynamic HTML documents programmatically. With a clean and intuitive API, LibDOM simplifies web development by allowing you to generate and manipulate HTML entirely in Python. Perfect for creating dynamic, maintainable, and responsive web pages.',
    packages=['libdom'],)