from setuptools import setup
import os

here = os.path.abspath(os.path.dirname(__file__))
# NEWS = open(os.path.join(here, 'NEWS.txt')).read()


version = '1.0.0'

setup(name='almanac',
      version=version,
      description='Solar event almanac',
      long_description='A solar event almanac, exposing JSON REST resources to search astronomical events for a time range',
      author='cghislai, inspired by Leslie P. Polzer',
      author_email='charlyghislain@gmail.com',
      url='http://github.com/cghislai/almanac/',
      license='MIT',
      classifiers=[
          # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
          "Development Status :: 4 - Beta"
          , "Environment :: Console"
          , "Intended Audience :: Science/Research"
          , "Intended Audience :: Developers"
          , "License :: OSI Approved :: MIT License"
          , "Operating System :: OS Independent"
          , "Programming Language :: Python :: 3"
          , "Topic :: Scientific/Engineering :: Astronomy"
          , "Topic :: Other/Nonlisted Topic"
          , "Topic :: Software Development :: Libraries :: Python Modules"
          , "Topic :: Utilities"
      ],
      maintainer='cghislai',
      maintainer_email='charlyghislain@gmail.com',
      packages=['almanac'],
      requires=['skyfield(>=1.9)'],
      extras_require={'Flask': ['flask']},
      entry_points={
          'console_scripts':
              ['almanac-server = almanac.http_server:main [Flask]']
      })
