##############################################################################
#
# Copyright (c) 2006 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
# This package is developed by the Zope Toolkit project, documented here:
# http://docs.zope.org/zopetoolkit
# When developing and releasing this package, please follow the documented
# Zope Toolkit policies as described by this documentation.
##############################################################################
"""Setup for zope.app.file package

"""
import os

from setuptools import find_packages
from setuptools import setup


def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()


setup(name='zope.app.file',
      version='5.0',
      author='Zope Foundation and Contributors',
      author_email='zope-dev@zope.org',
      description='File and Image -- Zope 3 Content Components',
      long_description=(
          read('README.rst')
          + '\n\n.. contents::\n\n' +
          read('src', 'zope', 'app', 'file', 'browser', 'file.rst')
          + '\n\n' +
          read('src', 'zope', 'app', 'file', 'browser', 'url.rst')
          + '\n\n' +
          read('CHANGES.rst')
      ),
      keywords="zope3 file image content",
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Zope Public License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
          'Programming Language :: Python :: 3.12',
          'Programming Language :: Python :: 3.13',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Topic :: Internet :: WWW/HTTP',
          'Framework :: Zope :: 3',
      ],
      url='https://github.com/zopefoundation/zope.app.file',
      license='ZPL 2.1',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['zope', 'zope.app'],
      python_requires='>=3.8',
      extras_require={
          'test': [
              'webtest',
              'zope.app.appsetup >= 4.0.0',
              'zope.app.basicskin >= 4.0.0',
              'zope.app.exception >= 4.0.1',
              'zope.app.folder >= 4.0.0',
              'zope.app.http >= 4.0.1',
              'zope.app.rotterdam >= 4.0.0',
              'zope.app.securitypolicy',
              'zope.app.wsgi >= 5.3',
              'zope.dublincore',
              'zope.login',
              'zope.principalannotation',
              'zope.publisher >= 3.12',
              'zope.testing',
              'zope.testrunner',
          ]
      },
      install_requires=[
          'setuptools',
          'transaction',
          'persistent',
          'zope.app.content >= 4.0.0',
          'zope.app.form >= 5.0.0',
          'zope.app.publication',
          'zope.contenttype >= 4.0.0',
          'zope.datetime',
          'zope.dublincore >= 4.0.0',
          'zope.event',
          'zope.exceptions',
          'zope.filerepresentation',
          'zope.i18nmessageid >= 4.1.0',
          'zope.interface',
          'zope.schema',
          'zope.site',
          'zope.size',
      ],
      include_package_data=True,
      zip_safe=False,
      )
