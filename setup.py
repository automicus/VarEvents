from setuptools import setup

setup(
    name='VarEvents',
    version='1.0.0',
    license='Apache License 2.0',
    url='http://automic.us/projects/pyisy',
    download_url='https://github.com/automicus/varevents/tarball/1.0.1',
    author='Ryan Kraus',
    author_email='automicus@gmail.com',
    description='Python module to create variables that can '
    + 'raise custom events.',
    packages=['VarEvents'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[],
    keywords=['event'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
