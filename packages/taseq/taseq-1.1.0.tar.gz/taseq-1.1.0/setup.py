#!/usr/bin/env python
from setuptools import setup, find_packages # type: ignore
from taseq.__init__ import __version__

setup(name='taseq',
      version=__version__,
      description='Downstream analysis for targetted amplicon sequencing.',
      author='Koki Chigira',
      author_email='kyoujin2009kutar@gmail.com',
      url='https://github.com/KChigira/taseq/',
      license='MIT',
      packages=find_packages(),
      install_requires=[
        'pandas',
        'matplotlib',
      ],
      entry_points={'console_scripts': [
            'taseq_hapcall = taseq.hapcall:main',
            'taseq_genotype = taseq.genotype:main',
            'taseq_filter = taseq.filter:main',
            'taseq_draw = taseq.draw:main',
            'taseq = taseq.default:main',
            ]
      }
    )
