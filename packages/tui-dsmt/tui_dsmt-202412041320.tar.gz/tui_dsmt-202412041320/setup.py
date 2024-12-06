import os
from datetime import datetime

from setuptools import setup, find_packages

version = os.environ['PACKAGE_VERSION']

setup(
    name='tui_dsmt',
    version=version,
    author='Eric Tröbs',
    author_email='eric.troebs@tu-ilmenau.de',
    description='everything you need for our jupyter notebooks',
    long_description='everything you need for our jupyter notebooks',
    long_description_content_type='text/markdown',
    url='https://dbgit.prakinf.tu-ilmenau.de/lectures/data-science-methoden-und-techniken',
    project_urls={},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.10',
    install_requires=[
        'jupyter',
        'ipywidgets',
        'checkmarkandcross',
        'fa2_modified==0.3.10',
        'ipyparallel==8.8.0',
        'matplotlib==3.9.2',
        'mlxtend==0.23.1',
        'mpi4py==3.1.6',
        'networkx==3.4.2',
        'numpy==1.26.4',  # scikit's PAM implementation does not work with NumPy >= 2
        'plotly==5.24.1',
        'pandas==2.2.3',
        'pyarrow==17.0.0',
        'pyfpgrowth==1.0',
        'pyspark==3.5.3',
        'scikit-learn==1.5.2',
        'scikit-learn-extra==0.3.0'
    ],
    package_data={
        'tui_dsmt': [
            'jpanim/resources/*',
            'clustering/resources/*',
            'fpm/resources/*',
            'graph/resources/*',
            'parallel/resources/*',
        ]
    },
    include_package_data=True
)
