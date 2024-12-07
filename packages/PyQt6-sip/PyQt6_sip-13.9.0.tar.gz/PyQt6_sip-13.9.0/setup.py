# SPDX-License-Identifier: BSD-2-Clause

# Copyright (c) 2024 Phil Thompson <phil@riverbankcomputing.com>


import glob

from setuptools import Extension, setup


# Build the extension module.
module_src = sorted(glob.glob('*.c'))

module = Extension('PyQt6.sip', module_src)

# Do the setup.
setup(
        name='PyQt6_sip',
        version='13.9.0',
        license='SIP',
        python_requires='>=3.8',
        ext_modules=[module]
     )
