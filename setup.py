from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from os import path

here = path.abspath(path.dirname(__file__))


setup(
    name='pyxp',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='1.0.0',

    description='A library for construct arithmetic expression in python, '
    'which could be serialize to and deserialize from string',
    long_description='',

    url='https://github.com/Xorcerer/pyxp',

    author='Logan Zhou',
    author_email='xorcererzc@gmail.com',

    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='math arithmetic expression AST abstract syntax tree serialization',

    packages=['pyxp'],

    install_requires=[],

    extras_require = {},

    package_data={},

    entry_points={},
)
