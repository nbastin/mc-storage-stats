# Copyright (c) 2021  Nick Bastin

import os
import os.path
from setuptools import setup, find_packages


setup(name = "mcstor",
      version = "0.1",
      author = "Nick Bastin",
      author_email = "nbastin@protonmail.com",
      packages = find_packages(),
      scripts = ['bin/storage-totals'],
      install_requires = [
        "anvil"
        ],
      classifiers = [
        "Programming Language :: Python :: 3.6",
        ],
      )

