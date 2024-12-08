from setuptools import setup, find_packages

with open('requirements.txt', 'r') as f:
    lines = [line.strip() for line in f.readlines()]

install_requires = [line for line in lines if line and not line.startswith('#')]

name = 'echobox'
version = '1.5.44'
author = 'kiuber'
author_email = 'kiuber.zhang@gmail.com'

packages = find_packages()
print(f'packages: {packages}')

setup(
    name=name,
    version=version,
    keywords=[name, author],
    description=name,
    license='',
    install_requires=install_requires,

    scripts=[],

    author=author,
    author_email=author_email,
    url='',

    packages=packages,
    platforms='any',
    # https://pypi.org/classifiers/
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows :: Windows 11",
    ]
)
