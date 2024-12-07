from setuptools import setup, find_packages
from os import path
from io import open
import ctypes
import logicqubit
import os
import sys

# sudo pip3 install twine
# python setup.py sdist
# python setup.py bdist_wheel
# twine upload dist/*
# sudo python setup.py install

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

def get_cupy_version():
    """
    Determines the appropriate cupy version based on the CUDA version.
    """
    cuda_version_map = {
        "12.": "cupy-cuda12x",
        "11.": "cupy-cuda11x",
        "10.2": "cupy-cuda102",
    }
    try:
        # Check CUDA version using nvcc
        cuda_version = os.popen("nvcc --version").read()
        for version, package in cuda_version_map.items():
            if version in cuda_version:
                return package
    except Exception as e:
        print(f"Warning: Unable to determine CUDA version. Using default cupy. Error: {e}", file=sys.stderr)

    return None

cupy_version = get_cupy_version()

requirements = ['sympy','numpy','matplotlib']
if cupy_version is not None:
    requirements.append(cupy_version)

setup(
    name='logicqubit-gpu',
    version=logicqubit.__version__,
    description='logicqubit-gpu is a simple library for quantum computing simulation with gpu acceleration.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/clnrp/logicqubit-gpu',
    author='Cleoner Pietralonga',
    author_email='cleonerp@gmail.com',

    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Physics',

        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=requirements,

)
