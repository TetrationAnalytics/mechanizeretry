from setuptools import setup

setup(
    name='mechanizeretry',
    version='1.2',
    install_requires=['mechanize'],
    packages=['mechanizeretry'],
    url='https://github.com/TetrationAnalytics/mechanizeretry',
    license='Apache 2.0',
    author='Mike Timm',
    author_email='mtimm@tetrationanalytics.com',
    description='Adds hang protection and retries to mechanize',
    keywords=['mechanize', 'retry'],
    classifiers=['Development Status :: 5 - Production/Stable'],
)
