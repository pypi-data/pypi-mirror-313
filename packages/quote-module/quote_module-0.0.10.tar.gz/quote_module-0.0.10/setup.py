import os
import subprocess
import setuptools
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

from quote_module import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()


class CMakeBuild(build_ext):
    def run(self):
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        # print(f'====> build_temp: {self.build_temp}')
        subprocess.check_call(['cmake', '../..', '-DCMAKE_BUILD_TYPE=Release'], cwd=self.build_temp)
        subprocess.check_call(['cmake', '--build', '.'], cwd=self.build_temp)
        # Move the built shared library to the expected location
        os.makedirs(self.build_lib, exist_ok=True)
        # print(dir(self))
        for ext in self.extensions:
            dest_path = self.get_ext_fullpath(ext.name)
            dest_dir = os.path.dirname(dest_path)
            dest_path = os.path.join(self.build_lib, 'quote_module', f'{ext.name}.so')
            src_path = os.path.join(self.build_temp, 'quote_module', f'{ext.name}.so')
            # print('get_ext_fullpath: ', self.get_ext_fullpath(''))
            # print('dir(ext) ', dir(ext))
            # print('get_outputs: ', self.get_outputs())
            print(f'\033[1;33mCopy {src_path} -> {dest_path} {ext.name}\033[0m')
            self.copy_file(src_path, dest_path)
            # raise ""

    def build_extension(self, ext):
        pass  # All the build work is done in run()


class bdist_wheel(_bdist_wheel):
    def finalize_options(self):
        _bdist_wheel.finalize_options(self)
        self.universal = False
        self.plat_name_supplied = True
        self.plat_name = 'manylinux2014_x86_64'


setup(
    name='quote_module',
    version=__version__,
    url='https://github.com/williamchen180/quote_module',
    author='William Chen',
    author_email='williamchen180@gmail.com',
    description='Your package description',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    # package_data={'mypylib': ['data/alert.wav']},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pandas', 'termcolor', 'requests', 'plotly', 'setuptools', 'matplotlib', 'numpy',
        'playsound', 'wheel', 'twine', 'cryptocode', 'line_notify', 'shioaji', 'pandasql', 'msgpack'
    ],
    ext_modules=[Extension('libquote_module', sources=[])],
    cmdclass={
        'build_ext': CMakeBuild,
        'bdist_wheel': bdist_wheel,
    },
    platforms=['linux_x86_64'],
)
