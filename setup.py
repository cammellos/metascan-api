try:
    from setuptools import setup

except ImportError:
    from distutils.core import setup

setup(
    name='metascan_api',
    test_suite="tests",
    version='1',
    packages=['metascan', 'metascan.tests'],
    url='https://github.com/blacktop/metascan-api',
    license='GPLv3',
    author='blacktop',
    author_email='',
    description='OPSWAT Metascan and Metascan Online API',
    install_requires=[
        "requests >= 2.2.1",
    ],
)
