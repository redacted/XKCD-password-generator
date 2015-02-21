from setuptools import setup


setup(
    name='xkcdpass',
    version='1.2.5',
    author='Steven Tobin',
    author_email='steventtobin@gmail.com',
    url='https://github.com/redacted/XKCD-password-generator',
    description='Generate secure multiword passwords/passphrases, inspired by XKCD',
    long_description=open('README.rst').read(),
    packages=['xkcdpass'],
    zip_safe=False,
    license='BSD',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'xkcdpass = xkcdpass.xkcd_password:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
    ],
)
