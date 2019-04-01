#!/usr/bin/env python3
import os
import re
import subprocess
import sys

from setuptools import setup, find_packages
from setuptools.command.install import install

# var = {}
# with open('sofa/__version__.py') as fp:
#     exec(fp.read(), var)

# This test is redundant given setuptools>=24.2.0 and pip>=9.0.0.
if sys.version_info < (3, 4):
    raise Exception('This project only supports Python 3.4+.')


def create_sofa_perf_timebase():

    dir_path = os.path.dirname(os.path.abspath(__file__))
    src_path = '{}/tools'.format(dir_path)

    cmd = "g++  {}/sofa_perf_timebase.cc -o {}/sofa/sofa_perf_timebase".format(src_path, dir_path)
    
    try:
        subprocess.check_call(cmd, cwd=src_path, shell=True)
    except subprocess.CalledProcessError:
        print("With command:{} failed.".format(cmd))


def create_cuhello():

    dir_path = os.path.dirname(os.path.abspath(__file__))
    src_path = '{}/tools'.format(dir_path)
    cmd = "nvcc {}/cuhello.cu -o {}/sofa/cuhello".format(src_path, dir_path)

    try:
        subprocess.check_call(cmd, cwd=src_path, shell=True, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print("No nvcc found; nvcc is required to improve perf timestamp accuracy.")
        pass




class CustomInstall(install):
    """Custom handler for the 'install' command."""
    def run(self):
        create_sofa_perf_timebase()
        create_cuhello()
        super().run()



setup(
        name='sofa',
        # version=var['__version__'],
        # description='',
        # long_description='',
        url='https://github.com/cyliustack/sofa',
        author='TODO',
        author_email='TODO',
        license='Apache',
        packages=find_packages('.'),
        classifiers=[
            'Development Status :: 2 - Pre-Alpha',

            'Intended Audience :: Developers',

            'License :: OSI Approved :: Apache Software License',

            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3 :: Only',
        ],
        # keywords='space-separated strings',
        install_requires=[
            'cxxfilt',
            'fuzzywuzzy',
            'matplotlib',
            'networkx',
            'numpy',
            'pandas',
            'python-Levenshtein',
            'requests',
            'sklearn',
            'sqlalchemy',


        ],
        python_requires='>=3.4',
        # tests_require=[
        # ],

        cmdclass={'install': CustomInstall},

        package_data={
            'sofa': ['../sofaboard/*', './sofa_perf_timebase', './cuhello'],
        },
        entry_points={
            'console_scripts': [
                'sofa = sofa.cli:main',
            ]
        },
        # setup_requires=['pytest-runner'],
)
