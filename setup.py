from setuptools import setup, find_namespace_packages
from io import open
import sys

setup(
    name='xkcdpass',
    version='1.19.7',
    author='Steven Tobin',
    author_email='steventtobin@gmail.com',
    url='https://github.com/redacted/XKCD-password-generator',
    description='Generate secure multiword passwords/passphrases, inspired by XKCD',
    long_description=open('README.rst', encoding='utf-8').read(),
    #packages=['xkcdpass'],
    packages=find_namespace_packages(exclude=["examples", "*.tests", "*.tests.*", "tests.*", "tests"]),
    zip_safe=False,
    license='BSD',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'xkcdpass = xkcdpass.xkcd_password:main',
        ],
    },
    tests_require=['mock'] if sys.version_info[0] == 2 else None,
    test_suite = 'tests',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
    ],
)
