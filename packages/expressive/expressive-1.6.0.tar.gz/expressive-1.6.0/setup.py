#!/usr/bin/env python3

""" Copyright 2024 Russell Fordyce

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from setuptools import setup

setup(
    name="expressive",
    version="1.6.0",
    description="A library for quickly applying symbolic expressions to NumPy arrays",
    url="https://gitlab.com/expressive-py/expressive",
    maintainer="Russell Fordyce",
    license="Apache License 2.0",
    keywords="sympy numba numpy",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Compilers",
    ],
    package_dir={"": "src"},
    py_modules=["expressive"],
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    python_requires=">=3.9",
    install_requires=[
        "sympy >= 1.13.2",
        "numpy >= 2.0.1",
        "numba >= 0.60.0",
        "llvmlite >= 0.43.0",
    ],
    #include_package_data=True,
    zip_safe=False,  # https://setuptools.pypa.io/en/latest/deprecated/zip_safe.html
)
