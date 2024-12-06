#!/usr/bin/env python3

import re

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


def get_version():
    with open('nextcaptcha/__init__.py', 'r') as f:
        return re.search(r'__version__ = ["\'](.*?)["\']', f.read()).group(1)


setup(name='nextcaptcha-python',
      version=get_version(),
      description='NextCaptcha Captcha Solving Service Api Wrapper for Python to solving recaptcha v2, v3,recapthcha moible,hcaptcha,funcaptcha',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/nextcaptcha/nextcaptcha-python/',
      install_requires=['requests'],
      author='nextcaptcha',
      author_email='support@nextcaptcha.com',
      packages=find_packages(),
      include_package_data=True,
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      python_requires='>=3.6',
      test_suite='tests')
