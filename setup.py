"""
Source build and installation script.
"""

from os import path, sep, walk
from pip.download import PipSession
from pip.req import parse_requirements
from setuptools import setup, find_packages

version = '0.0.1-dev'


def extract_requirements(filename):
    return [str(r.req) for r in parse_requirements(filename, session=PipSession)]


def find_package_data(source, strip=''):
    pkg_data = []
    for root, dirs, files in walk(source):
        pkg_data += map(
            lambda f: path.join(root.replace(strip, '').lstrip(sep), f),
            files
        )
    return pkg_data


base_dir = path.dirname(__file__)

with open(path.join(base_dir, 'README.md')) as f:
    long_description = f.read()

install_requires = extract_requirements('requirements.txt')

setup(
    name='stratux',
    version=version,
    description='Stratux visualiser',
    long_description=long_description,
    license='MIT',
    url='https://github.com/frankzhao/stratux',
    author='Frank Zhao',
    author_email='frank@frankzhao.net',
    classifiers=[
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    packages=find_packages(),
    scripts=['bin/stratux'],
    install_requires=install_requires,
)
