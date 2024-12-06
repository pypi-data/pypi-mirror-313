# --------------------------------------------
# Copyright 2021, Roberto Himmelbauer
# @Author: Roberto Himmelbauer
# @Date:   2021-11-09
# --------------------------------------------

from os import path
from setuptools import setup, find_packages

from user_notifications.__version__ import VERSION

readme_file = path.join(path.dirname(path.abspath(__file__)), 'README.md')

try:
    from m2r import parse_from_file
    long_description = parse_from_file(readme_file)     # Convert the file to RST for PyPI
except ImportError:
    # m2r may not be installed in user environment
    with open(readme_file) as f:
        long_description = f.read()


package_metadata = {
    'name': 'django-user-notifications',
    'version': VERSION,
    'description': 'Django App that extendes django-user-messages for createing easy user notifications based user set rules.',
    'long_description': long_description,
    'url': 'https://github.com/rhimmelbauer/django-user-notifications/',
    'author': 'Roberto Himmelbauer',
    'author_email': 'robertoh89@gmail.com',
    'license': 'MIT license',
    'classifiers': [
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.8',
    ],
    'keywords': ['django', 'app', 'messages'],
}

setup(
    packages=find_packages(),
    package_data={'user_notifications': ['templates/user_notifications/*.html', 'templates/user_notifications/*/*.html']},
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=[
        'Django>=3.0,<4.0',
        'django-autoslug',
        'django-extensions',
        "django-user-messages",
        'iso4217',
    ],
    extras_require={
        'dev': [
            'dj-database-url',
            'psycopg2-binary',
            'django-crispy-forms',
            'django-allauth',
        ],
        'test': [],
        'prod': [],
        'build': [
            'setuptools',
            'wheel',
            'twine',
            'm2r',
            'keyrings.google-artifactregistry-auth'
        ],
        'docs': [
            'recommonmark',
            'm2r',
            'django_extensions',
            'coverage',
            'Sphinx',
            'rstcheck',
            'sphinx-rtd-theme'
        ],
    },
    **package_metadata
)