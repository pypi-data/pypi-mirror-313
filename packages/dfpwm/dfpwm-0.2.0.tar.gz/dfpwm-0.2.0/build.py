import os
import sys

import numpy
from setuptools import Extension
from setuptools.command.build_ext import build_ext
from setuptools.errors import CCompilerError, ExecError, PlatformError

CYTHON = False
try:
    from Cython.Build import cythonize

    CYTHON = True
except ImportError:
    print("Cython not found")

SOURCE_EXT = os.environ.get('SOURCE_EXT', 'pyx' if CYTHON else 'c')

file_ext = SOURCE_EXT

build_modules = ['convertor']

extensions = [
    Extension(f'dfpwm.{module}', [f'./dfpwm/{module}.{file_ext}'])
    for module in build_modules
]

include_dirs = [
    numpy.get_include()
]


class ExtBuilder(build_ext):
    def run(self):
        try:
            super().run()
        except FileNotFoundError as e:
            raise Exception("File not found, could not build extension") from e
        except PlatformError:
            raise

    def build_extension(self, ext):
        try:
            super().build_extension(ext)
        except (CCompilerError, ExecError, PlatformError, ValueError) as e:
            raise Exception('Could not compile C extension.') from e


def build(setup_kwargs: dict):
    os.environ['CFLAGS'] = '-O3'

    if not CYTHON and SOURCE_EXT == 'pyx':
        raise Exception("Cannot compile pyx without Cython")

    setup_kwargs.update({
        'ext_modules': cythonize(
            extensions, language_level=3,
            compiler_directives={'linetrace': True}
        ) if SOURCE_EXT == 'pyx' else extensions, "include_dirs": include_dirs,
        "cmdclass": {
            "build_ext": ExtBuilder,
        }
    })



if __name__ == '__main__':
    params = sys.argv[1:]
    if len(params) != 0 and 'build' == params[0]:
        if not CYTHON:
            print("Please install cython to convert to .c file")
            sys.exit(-1)

        if SOURCE_EXT == 'pyx':
            cythonize([f'./dfpwm/{module}.pyx' for module in build_modules])
        else:
            print("SOURCE_EXT must be 'pyx'")
else:
    if CYTHON:
        cythonize([f'./dfpwm/{module}.pyx' for module in build_modules])