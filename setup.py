from setuptools import setup
from setuptools import find_packages


SETUP = {
    'name': 'equity',
    'version': '0.1',
    'packages': ['equity'],
    'install_requires': [],
    'author': 'Bobby R. Ward',
    'author_email': 'bobbyrward@gmail.com',
    'description': 'A git stash alternative for subversion with an emphasis on safety',
    'license': 'GPL',
    'keyworks': 'svn subversion stash equity',
    'url': 'http://github.com/bobbyrward/equity',
    'entry_points': {
        'console_scripts': {
            'equity = equity.commands:main',
        }
    },
}


setup(**SETUP)
