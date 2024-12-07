#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

packages_pheasy = [
    "pheasy",
    "pheasy.core",
    "pheasy.interface",
    "pheasy.structure",
]

scripts_pheasy = ["scripts/pheasy"]

setup(
    name="pheasy",
    version="0.0.2",
    description="A calculator for high-order force constants and phonon quasiparticles.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://gitlab.com/cplin/pheasy",
    maintainer="Changpeng Lin",
    maintainer_email="changpeng.lin@epfl.ch",
    packages=packages_pheasy,
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    install_requires=[
        "ase>=3.22.1",
        "f90nml>=1.3.1",
        "spglib>=1.16.3",
        "numpy>=1.11.0",
        "scipy>=1.4.1",
        "scikit-learn>=1.0.2",
    ],
    scripts=scripts_pheasy,
)
