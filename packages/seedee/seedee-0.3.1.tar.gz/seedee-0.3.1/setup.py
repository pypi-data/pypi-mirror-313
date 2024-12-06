#!/usr/bin/python3

import io
import os

from setuptools import setup, find_namespace_packages
from setuptools.extension import Extension
from Cython.Build import cythonize
import numpy as np

# Package meta-data.
NAME = 'seedee'
DESCRIPTION = 'A (de)serialization library for multidimensional arrays'
URL = 'https://gitlab.desy.de/fs-sc/seedee'
EMAIL = 'tim.schoof@desy.de'
AUTHOR = 'Tim Schoof'
REQUIRES_PYTHON = '>=3.6'
VERSION = "0.3.1"

# What packages are required for this module to be executed?
REQUIRED = [
    'numpy',
]

# What packages are optional?
EXTRAS = {
    "tests": ['pytest', 'h5py', 'hdf5plugin']
}


# The rest you shouldn't have to touch too much :)
# ------------------------------------------------

here = os.path.abspath(os.path.dirname(__file__))


# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except IOError:
    long_description = DESCRIPTION


# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    with open(os.path.join(here, NAME, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


libraries = ["seedee"]
macros = [("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")]

if os.environ.get("SEEDEE_WHEEL_INCLUDE_LIB", "off").lower() in ["on", "true"]:
    print("INFO: including seedee library in wheel")
    runtime_library_dirs = ["$ORIGIN/lib"]
    package_data = {"seedee.lib": ["*.so*"]}
else:
    runtime_library_dirs = []
    package_data = {}

extensions = [
    Extension(
        "seedee.seedee_wrapper",
        ["src/seedee/seedee_wrapper.pyx"],
        include_dirs=[np.get_include(), "include"],
        libraries=libraries,
        library_dirs=["lib"],
        define_macros=macros,
        extra_compile_args=["-O3"],
        extra_link_args=['-Wl,--exclude-libs,ALL'],
        runtime_library_dirs=runtime_library_dirs,
    )]

# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_namespace_packages("src", exclude=('tests',)),
    package_dir={'': 'src'},
    ext_modules=cythonize(extensions),
    zip_safe=False,
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    package_data=package_data,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: Implementation :: CPython',
        'Development Status :: 4 - Beta',
    ],
)
