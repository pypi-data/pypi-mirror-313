# Author: Shinji Uetsuki <greenroom1973@gmail.com>
# Copyright (c) 2024 Shinji Uetsuki
# License: MIT

from setuptools import setup
import sp_lib

DESCRIPTION = "sp_lib: please see README"
NAME = 'sp_lib'
AUTHOR = 'Shinji Uetsuki'
AUTHOR_EMAIL = 'greenroom1973@gmail.com'
URL = 'https://github.com/greenroomy/amazon_sp_api'
LICENSE = 'MIT license'
DOWNLOAD_URL = 'https://github.com/greenroomy/amazon_sp_api/'
VERSION = sp_lib.__version__
PYTHON_REQUIRES = ">=3.8"

INSTALL_REQUIRES = [
    'requests>=2.28.2',
    'pandas>=1.5.3',
    'urllib3>=1.26.15',
    'pandas>=1.2.4',
]

PACKAGES = [
    'sp_lib'
]

with open('README.md', 'r') as fp:
    readme = fp.read()
with open('CONTACT.txt', 'r') as fp:
    contacts = fp.read()
long_description = readme + '\n\n' + contacts

setup(name=NAME,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      maintainer=AUTHOR,
      maintainer_email=AUTHOR_EMAIL,
      description=DESCRIPTION,
      long_description=long_description,
      license=LICENSE,
      url=URL,
      version=VERSION,
      download_url=DOWNLOAD_URL,
      python_requires=PYTHON_REQUIRES,
      install_requires=INSTALL_REQUIRES,
      packages=PACKAGES
      )

