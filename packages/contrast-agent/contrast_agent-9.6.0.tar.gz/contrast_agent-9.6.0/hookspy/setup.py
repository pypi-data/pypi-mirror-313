#!/usr/bin/env python
import os
from glob import glob
from setuptools import setup, find_packages, Extension


extension_dir = "ext"
c_sources = glob(os.path.join(extension_dir, "*.c"))


extensions = [
    Extension(
        "hookspy.hookspy",
        c_sources,
        include_dirs=[extension_dir],
        extra_compile_args=[
            "-Wall",
            "-Wextra",
            "-Werror",
            "-Wno-unused-parameter",
            "-Wmissing-field-initializers",
        ],
    )
]


setup(
    name="hookspy",
    version="0.1.0",
    description="Find hook locations for python objects",
    url="",
    author="Dan D'Avella",
    author_email="daniel.davella@contrastsecurity.com",
    package_dir={"": "src"},
    packages=find_packages("src"),
    ext_modules=extensions,
    entry_points={"console_scripts": ["hookspy-autogen=hookspy:autogen_main"]},
)
