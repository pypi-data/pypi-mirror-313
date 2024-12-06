from setuptools import setup, Extension, find_packages
import numpy
import os
import sys


# This is all the cpp files that need compiling
# This could be automated by just scanning ../src for cpp files, but this way me be safer
sources = ['cg_iter', 'lsmr_iter', 'op_main', 'gropt_params', 'optimize', 'gropt_utils',
           'op_gradient',  'op_moments', 'op_slew', 'op_girfec_pc', 'op_duty', 'op_sqdist', 'op_fft_sqdist', 'op_eddy', 'op_pns', 'op_safe',
           'op_bval', 'logging', 'fft_helper', 'solver', 'minres_iter', 'minresqlp_iter', 'linesearch']

sourcefiles = ['./cython_src/gropt2.pyx',] + ['./src/%s.cpp' % x for x in sources]


include_dirs = [".",  "./src", numpy.get_include(),]
library_dirs = [".", "./src",]

libraries = []

include_dirs.append("./src/fftw3/")

if sys.platform == 'darwin':
    library_dirs.append("/opt/homebrew/lib/")
    libraries.append("fftw3")
elif sys.platform == 'win32':
    library_dirs.append("C:\\fftw3\\")
    libraries.append("libfftw3-3")


include_dirs = [os.path.abspath(x) for x in include_dirs]
library_dirs = [os.path.abspath(x) for x in library_dirs]


extra_compile_args = ['-std=c++11']
extra_link_args = []


cython_ext = Extension("gropt2",
                sourcefiles,
                language = "c++",
                libraries=libraries,
                include_dirs = include_dirs,
                library_dirs = library_dirs,
                extra_compile_args = extra_compile_args,
                extra_link_args = extra_link_args,
                # undef_macros=['NDEBUG'], # This will *re-enable* the Eigen assertions
            )


setup(
    name='gropt2',
    version="0.0.23",
    setup_requires=[
        'setuptools>=18.0',  # first version to support pyx in Extension
        'cython>=0.18',
    ],
    ext_modules=[cython_ext],
)