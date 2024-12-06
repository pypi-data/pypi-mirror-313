# Updated setup.py for MacOS stock LLVM compilation, but I would like to
# add some type of homebrew gcc detection for openmp . . . 
import os, sys

def is_platform_windows():
    return sys.platform == "win32"

def is_platform_mac():
    return sys.platform == "darwin"

try:
    from setuptools import setup
    from setuptools import Extension
except ImportError:
    from distutils.core import setup
    from distutils.extension import Extension

from Cython.Build import cythonize
import numpy

# This is all the cpp files that need compiling
# This could be automated, but this is safer
sources = ['cg_iter', 'lsmr_iter', 'op_main', 'gropt_params', 'optimize', 'gropt_utils',
           'op_gradient',  'op_moments', 'op_slew', 'op_girfec_pc', 'op_duty', 'op_sqdist', 'op_fft_sqdist', 'op_eddy', 'op_pns',
           'op_bval', 'logging',
           'fft_helper']

sourcefiles = ['./cython_src/gropt2.pyx',] + ['../src/%s.cpp' % x for x in sources]

include_dirs = [".",  "../src", numpy.get_include(),]
library_dirs = [".", "../src",]

include_dirs.append("C:\\fftw3\\")
library_dirs.append("C:\\fftw3\\")
libraries = ["libfftw3-3",]

# include_dirs.append("C:\\Program Files (x86)\\Intel\\oneAPI\\mkl\\latest\\include")
# include_dirs.append("C:\\Program Files (x86)\\Intel\\oneAPI\\mkl\\latest\\include\\fftw")
# library_dirs.append("C:\\Program Files (x86)\\Intel\\oneAPI\\mkl\\latest\\lib\\intel64")
# library_dirs.append("C:\\Program Files (x86)\\Intel\\oneAPI\\compiler\\latest\\windows\\compiler\\lib\\intel64_win")
# libraries = ["mkl_core","mkl_sequential", "mkl_intel_lp64", "mkl_intel_thread","libiomp5md"]


include_dirs = [os.path.abspath(x) for x in include_dirs]
library_dirs = [os.path.abspath(x) for x in library_dirs]


# openmp stufff here
if is_platform_windows:
    extra_compile_args = ["/openmp",]
    extra_link_args = []
else:
    extra_compile_args = []
    extra_link_args = []



extensions = [Extension("gropt2",
                sourcefiles,
                language = "c++",
                libraries=libraries,
                include_dirs = include_dirs,
                library_dirs = library_dirs,
                extra_compile_args = extra_compile_args,
                extra_link_args = extra_link_args,
                undef_macros=['NDEBUG'], # This will re-enable the Eigen assertions
            )]

setup(
    name = "gropt2",
    ext_modules = cythonize(extensions,
                  compiler_directives={'language_level' : sys.version_info[0]}),
    include_dirs = include_dirs
)