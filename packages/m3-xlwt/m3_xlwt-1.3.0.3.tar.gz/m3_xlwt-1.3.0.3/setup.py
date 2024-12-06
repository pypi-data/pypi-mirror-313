import os

from setuptools import find_packages, setup

setup(
    name='m3-xlwt',
    version='1.3.0.3',
    url='https://stash.bars-open.ru/projects/M3/repos/m3-xlwt/browse',
    license='Apache License, Version 2.0',
    author='BARS Group',
    author_email='a.danilenko@bars.group',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    description='Патч официальной библиотеки xlwt для работы с excel-файлами',
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Natural Language :: Russian',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
