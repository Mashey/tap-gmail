#!/usr/bin/env python

from setuptools import setup

setup(name='tap-gmail',
      version='0.0.1',
      description='Singer.io tap for extracting data from the Zoom API',
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      py_modules=['tap_gmail'],
      install_requires=[
        'singer-python==5.9.0',
        'cchardet==2.1.6',
        'python-dotenv==0.14.0',
        'pyyaml==5.3.1',
        'vcrpy==4.1.0',
        'pytest-vcr==1.0.2',
        'coverage==5.3',
        'pytest-cov==2.10.1',
        'singer-python==5.9.0',
        'requests',
        'google-auth==1.23.0',
        'google-auth-httplib2==0.0.4',
        'google-api-python-client==1.12.5',
        'google-auth-oauthlib==0.4.2',
        'oauth2client==4.1.3'
      ],
      entry_points='''
          [console_scripts]
          tap-gmail=tap_gmail:main
      ''',
      packages=['tap_gmail'],
      package_data = {
          'tap_gmail': ['schemas/*.json'],
      }
)