#!/usr/bin/env python 
# 不用numpy不加这行
#from numpy.distutils.core import Extension as NumpyExtension
#from numpy.distutils.core import setup

#from distutils.extension import Extension
#from Cython.Build import cythonize

import numpy
from distutils.core import setup  
# 必须部分
from distutils.extension import Extension  
# 必须部分
from Cython.Distutils import build_ext 


setup(
    name='minirf',
    version='0.2.3',
    description='Calculate miniRF',
    author='none',
    author_email="noe",
    url="none",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    package_dir={
        'minirf': 'src'
    },
    packages=[
        'minrf',
    ],
    cmdclass={"build_ext": build_ext},
    ext_modules=[
        Extension(
            name='rfmini',
            extra_f77_compile_args='-O3 -ffixed-line-length-none -fbounds-check -m64'.split(),
            sources=[
        "rfmini.pyx",
        "greens.cpp",
        "model.cpp",
        "pd.cpp",
        "synrf.cpp",
        "wrap.cpp",
        "fork.cpp"],
            include_dirs=[numpy.get_include()]# noqa
            )
        ]
)