from setuptools import setup, find_packages

setup(
    name='VarEvents',
    version='1.0.0',
    license='Apache License 2.0',
    url='http://automic.us/projects/pyisy',
    author='Ryan Kraus',
    author_email='automicus@gmail.com',
    description='Python module to create variables that can '
    + 'raise custom events.',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License 2.0',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
