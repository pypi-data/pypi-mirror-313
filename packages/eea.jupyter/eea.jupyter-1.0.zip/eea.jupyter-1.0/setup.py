""" eea.jupyter Installer
"""
import os
from os.path import join

from setuptools import find_packages, setup

NAME = "eea.jupyter"
PATH = NAME.split(".") + ["version.txt"]

with open(join(*PATH)) as f:
    VERSION = f.read().strip()
with open("README.rst") as f:
    README = f.read()
with open(os.path.join("docs", "HISTORY.txt")) as f:
    HISTORY = f.read()

setup(
    name=NAME,
    version=VERSION,
    description="eea.jupyter utilities for jupyter notebook",
    long_description_content_type="text/x-rst",
    long_description=(
        README + "\n" +
        HISTORY
    ),
    classifiers=[
        "Environment :: Web Environment",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords='EEA Utilities',
    author='European Environment Agency: IDM2 A-Team',
    author_email='eea-edw-a-team-alerts@googlegroups.com',
    url='https://github.com/eea/eea.banner',
    license='GPL version 2',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['eea'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
    ]
)
