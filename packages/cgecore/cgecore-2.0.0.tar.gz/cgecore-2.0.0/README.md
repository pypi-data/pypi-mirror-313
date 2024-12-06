# CGE Core Module version 2 released

The cgecore module have been updated to version 2.0.0. Despite earlier announcements, we have decided  to try and keep most of the legacy functionality in version 2. All CGE tools should work with this updated version. However, we did not have the resources to test it with all CGE tools.
This version includes all functionality from the [cgelib package version 0.7.5](https://bitbucket.org/genomicepidemiology/cgelib). The cgelib package has been deprecated and all functionality has been moved to the cgecore package. The cgecore package is now the one-stop core module for the Center for Genomic Epidemiology.

**Please note that some parts of the added functionality is still in development and tests are far from complete.**

# cge_core_module

Core module for the Center for Genomic Epidemiology

This module contains classes and functions needed to run the service wrappers and pipeline scripts

The pypi project can be found here:
https://pypi.org/project/cgecore/

# How to update:
1. Make changes to the modules
2. Bump the version number accordingly in cgecore/__init__.py
3. Install package locally
4. Test the changes locally (for both python2 and python3)
5. Distribute to Pypi

# Install package locally
python2 setup.py install

python3 setup.py install

# Distribute to PyPi
python3 setup.py sdist bdist_wheel

twine upload dist/*

*deprecated:*
~~python setup.py sdist upload -r pypi~~
