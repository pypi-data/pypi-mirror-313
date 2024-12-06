# coding: utf-8
import os

from setuptools import find_packages
from setuptools import setup


setup(
    name='concentrator',
    author="BARS Group",
    description='Concentrator',
    url='https://stash.bars-open.ru/projects/EDUKNDG/repos/concentrator/',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=(
        'm3-builder>=1.2.0,<2',
        'pylatex==1.4.1',
        'python-magic>=0.4.15,<0.5'
    ),
    include_package_data=True,
    dependency_links=('http://pypi.bars-open.ru/simple/m3-builder', ),
    setup_requires=('m3-builder>=1.2.0,<2', ),
    set_build_info=os.path.dirname(__file__),
)
