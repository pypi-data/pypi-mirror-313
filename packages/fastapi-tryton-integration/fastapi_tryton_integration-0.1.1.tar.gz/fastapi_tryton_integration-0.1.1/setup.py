# This file is part of fastapi_tryton_integration.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
import io
import os
import re

from setuptools import setup


def read(fname):
    return io.open(
        os.path.join(os.path.dirname(__file__), fname),
        'r', encoding='utf-8').read()


def get_version():
    init = read('fastapi_tryton.py')
    return re.search("__version__ = '([0-9.]*)'", init).group(1)


setup(
    name='fastapi_tryton_integration',
    version=get_version(),
    description='Adds Tryton support to FastAPI application',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',  # Especifica el formato como Markdown
    author='Solutema',
    author_email='info@solutema.com',
    url='https://pypi.org/project/fastapi-tryton-integration/',
    download_url='https://code.gruposolutema.com/fastapi-tryton-integration/',
    project_urls={
        "Source Code": 'https://code.gruposolutema.com/fastapi-tryton-integration',
    },
    py_modules=['fastapi_tryton_integration'],
    zip_safe=False,
    platforms='any',
    keywords='fastapi tryton web',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Tryton',
        'Framework :: FastAPI',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    license='GPL-3',
    python_requires='>=3.10',
    install_requires=[
        'fastapi<=0.115.6',
        'trytond>=6.0',
    ],
)
