import os
from setuptools import setup
from distutils.extension import Extension
from Cython.Build import cythonize
from torch.utils.cpp_extension import BuildExtension
import numpy

# Use /usr/bin/clang and /usr/bin/clang++
os.environ["CC"] = "/usr/bin/clang"
os.environ["CXX"] = "/usr/bin/clang++"

# Get the numpy include directory
numpy_include_dir = numpy.get_include()

# Extensions
pykdtree = Extension(
    'src.utils.libkdtree.pykdtree.kdtree',
    sources=[
        'src/utils/libkdtree/pykdtree/kdtree.c',
        'src/utils/libkdtree/pykdtree/_kdtree_core.c'
    ],
    language='c',
    extra_compile_args=['-std=c99', '-O3'],  # Removed '-fopenmp'
    include_dirs=[numpy_include_dir]
)

mcubes_module = Extension(
    'src.utils.libmcubes.mcubes',
    sources=[
        'src/utils/libmcubes/mcubes.pyx',
        'src/utils/libmcubes/pywrapper.cpp',
        'src/utils/libmcubes/marchingcubes.cpp'
    ],
    language='c++',
    extra_compile_args=['-std=c++11'],
    include_dirs=[numpy_include_dir]
)

triangle_hash_module = Extension(
    'src.utils.libmesh.triangle_hash',
    sources=[
        'src/utils/libmesh/triangle_hash.pyx'
    ],
    libraries=['m'],  # Unix-like specific
    include_dirs=[numpy_include_dir]
)

mise_module = Extension(
    'src.utils.libmise.mise',
    sources=[
        'src/utils/libmise/mise.pyx'
    ],
)

simplify_mesh_module = Extension(
    'src.utils.libsimplify.simplify_mesh',
    sources=[
        'src/utils/libsimplify/simplify_mesh.pyx'
    ],
    include_dirs=[numpy_include_dir]
)

from Cython.Build import cythonize

voxelize_module = Extension(
    'src.utils.libvoxelize.voxelize',
    sources=[
        'src/utils/libvoxelize/voxelize.pyx'
    ],
    libraries=['m'],  # Unix-like specific
    include_dirs=[numpy_include_dir],
    extra_compile_args=['-std=c99'],  # Ensure correct C flag
)


# Gather all extension modules
ext_modules = [
    pykdtree,
    mcubes_module,
    triangle_hash_module,
    mise_module,
    simplify_mesh_module,
    voxelize_module,
]

setup(
    ext_modules=cythonize(ext_modules, compiler_directives={'language_level': '3'}),
    cmdclass={
        'build_ext': BuildExtension.with_options(use_ninja=False)  # Disable Ninja
    }
)
