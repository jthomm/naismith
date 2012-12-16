import naismith

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='naismith',
      version=naismith.__version__,
      description='A basketball data collection and analysis tool for Python'
      author='jthomm',
      author_email='jthomm@yahoo.com',
      packages=['naismith'],
      license='MIT',
      classifiers=('Programming Language :: Python',
                   'Programming Language :: Python 2.7',),)
