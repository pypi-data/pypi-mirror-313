from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext
from Cython.Build import cythonize
import numpy

# 定义 Cython 扩展模块
extensions = [
    Extension(
        'GQuery.rfmini.rfmini',  # 模块名
        sources=['GQuery/rfmini/rfmini.pyx',
                 "GQuery/rfmini/greens.cpp",
                "GQuery/rfmini/model.cpp",
                "GQuery/rfmini/pd.cpp",
                "GQuery/rfmini/synrf.cpp",
                "GQuery/rfmini/wrap.cpp",
                "GQuery/rfmini/fork.cpp"],  # 指定 Cython 源文件路径
        extra_f77_compile_args='-O3 -ffixed-line-length-none -fbounds-check -m64'.split(),  
        include_dirs=[numpy.get_include()]# 其他编译参数（可选）
    ),
]

setup(
    name='GQuery',                              # 包名
    version='0.1.1',
    packages=find_packages(),
    ext_modules=cythonize(extensions), 
    cmdclass={"build_ext": build_ext},# 使用 cythonize 进行编译
    zip_safe=False,  
    install_requires=[
        'keras==3.2.1',          # 指定版本要求的依赖
        'dispCal',               # 默认最新版本
        'torch', 
        'scipy',
        'numpy',
        'matplotlib',
        'netCDF4'# 指定版本范围
    ],# 防止打包为 .egg 格式
    # 其他配置项
)
