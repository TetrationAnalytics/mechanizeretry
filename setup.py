from setuptools import setup

setup(
    name='mechanizeretry',
    version='1.4',
    install_requires=['mechanize'],
    packages=['mechanizeretry'],
    url='https://github.com/TetrationAnalytics/mechanizeretry',
    license=open('LICENSE.txt').read(),
    author='Mike Timm',
    author_email='mtimm@tetrationanalytics.com',
    description='Adds hang protection and retries to mechanize',
    long_description=open('README.rst').read(),
    keywords=['mechanize', 'retry'],
    classifiers=['Development Status :: 5 - Production/Stable'],
)
