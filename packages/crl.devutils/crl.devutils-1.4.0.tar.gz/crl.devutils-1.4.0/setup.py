import os
import sys
from setuptools import setup, find_packages

__copyright__ = 'Copyright (C) 2019-2024, Nokia'

VERSIONFILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'src', 'crl', 'devutils', '_version.py')


def import_module(name, path):
    if sys.version_info.major == 2:
        import imp
        return imp.load_source(name, path)

    import importlib
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def get_version():
    return import_module('_version', VERSIONFILE).get_version()


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(
    name='crl.devutils',
    version=get_version(),
    author='Petri Huovinen',
    author_email='petri.huovinen@nokia.com',
    description='Common Robot Libraries development and CI tools',
    install_requires=['invoke==0.12.2',
                      'check-manifest==0.41',
                      'devpi-client==5.2.3',
                      'tox==3.24.5',
                      'future',
                      'six',
                      'rstcheck',
                      'setuptools==68.2.2;python_version>="3.10"',
                      'sphinx<7.0',
                      'Jinja2==3.0.3;python_version>"3.0"',
                      'robotframework',
                      'virtualenvrunner',
                      'virtualenv==20.13.4',
                      'configparser'],
    long_description=read('README.rst'),
    license='BSD 3-Clause',
    classifiers=['Intended Audience :: Developers',
                 'License :: OSI Approved :: BSD License',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: 3.8',
                 'Programming Language :: Python :: 3.9',
                 'Programming Language :: Python :: 3.10',
                 'Topic :: Software Development'],
    keywords='robotframework testing testautomation acceptancetesting atdd bdd',
    url='https://github.com/nokia/crl-devutils',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['crl'],
    entry_points={
        'console_scripts': [
            'crl = crl.devutils.tasks:main']}
)
