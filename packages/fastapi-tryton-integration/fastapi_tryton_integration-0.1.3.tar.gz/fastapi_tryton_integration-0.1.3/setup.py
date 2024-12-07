import io
import os
import re

import setuptools

def read(fname):
    return io.open(
        os.path.join(os.path.dirname(__file__), fname),
        'r', encoding='utf-8').read()
        
setuptools.setup(
    name='fastapi_tryton_integration',
    version='0.1.3',
    author='Solutema SRL',
    description='FastAPI connection module for Tryton ERP',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    packages=['fastapi_tryton_integration', ],
    )