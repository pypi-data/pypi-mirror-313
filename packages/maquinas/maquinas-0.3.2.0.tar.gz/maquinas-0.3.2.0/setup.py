from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'maquinas',
  packages = ['maquinas','maquinas.regular','maquinas.contextfree','maquinas.parser','maquinas.contextsensitive','maquinas.recursivelyenumerable'],
  version = '0.3.2.0',
  license='GNU General Public License v3 or later',
  description = 'Formal languages and automata library',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Ivan Vladimir Meza Ruiz',
  author_email = 'ivanvladimir+maquinas@gmail.com',
  url = 'https://gitlab.com/ivanvladimir/maquinas',
  download_url = 'https://gitlab.com/ivanvladimir/maquinas/-/archive/0.3.2.0/maquinas-0.3.2.0.zip',
  keywords = ['regular languages', 'context free languages', 'context sensitive languages', 'recursively enumerable languages'],
  install_requires=[
          'graphviz',
          'ipywidgets',
          'IPython',
          'ordered_set',
          'Pillow',
          'TatSu'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Education',
    'Topic :: Education',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.8',
  ],
)
