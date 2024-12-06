"""
A setuptools based setup module.
Based on:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

import sys

import yaml
import setuptools  # type: ignore


def get_version(version_file_loc):
    with open(version_file_loc, 'r') as stream:
        data = yaml.load(stream, yaml.SafeLoader)
        return (data.get('version'))


def inject_custom_repository(repository_name):
    blacklist = ['register', 'upload']
    inject_arg = '--repository=%s' % (repository_name)

    for command in blacklist:
        try:
            index = sys.argv.index(command)
        except ValueError:
            continue

        sys.argv.insert(index + 1, inject_arg)


inject_custom_repository('orbital')

EXCLUDE_FILES = []

setuptools.setup(
    name='terrascope-api',
    version=get_version('ops/conda-recipe/conda_build_config.yaml'),
    description='Terrascope API Client',
    url='https://github.com/orbitalinsight/oi_papi',
    package_dir={'': 'src/py'},
    packages=setuptools.find_packages('src/py', exclude=[
        'mocked_services',
        'oi_papi',
        'oi_papi.*'
    ]),
    install_requires=['grpcio', 'grpcio-status', 'requests']
)
