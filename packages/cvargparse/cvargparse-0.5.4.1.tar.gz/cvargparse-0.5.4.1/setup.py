#!/usr/bin/env python

from pathlib import Path

from setuptools import setup, find_packages

try: # for pip >= 10
	from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
	from pip.req import parse_requirements
pkg_name = "cvargparse"

cwd = Path(__file__).parent.resolve()
# Get __version__ variable
with open(str(cwd / pkg_name / '_version.py')) as version_file:
	exec(version_file.read())

install_requires = [line.strip() for line in open("requirements.txt").readlines()]

setup(
	name=pkg_name,
	version=__version__,  # noqa: F821
	description='simple argparse wrapper with some syntactic sugar',
	author='Dimitri Korsch, Christoph Theiß',
	author_email='korschdima@gmail.com, theisz.cm@gmail.com',
	license='MIT License',
	packages=find_packages(),
	zip_safe=False,
	setup_requires=[],
	# no requirements yet
	install_requires=install_requires,
	package_data={'': ['requirements.txt']},
	data_files=[('.',['requirements.txt'])],
	include_package_data=True,
)
