"""
TI SimpleLink CRC tool

Tool to insert CRCs into ELF files or generate binary for programming
ccfg user region

Copyright (C) 2024 Texas Instruments Incorporated


 Redistribution and use in source and binary forms, with or without
 modification, are permitted provided that the following conditions
 are met:

   Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.

   Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the
   distribution.

   Neither the name of Texas Instruments Incorporated nor the names of
   its contributors may be used to endorse or promote products derived
   from this software without specific prior written permission.

 THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""


import logging
import setuptools
import re
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

version_file = (this_directory / "version_number.txt")

if version_file.is_file():
    logging.info("Reading version number from file %s", version_file.resolve())
    version_number = version_file.read_text()
else:
    logging.error("Could not find version file: %s", version_file)
    version_number = "1.00.00.00"
    logging.info("Using default version number of %s", version_number)
    with open("version_number.txt", "w") as version_file:
        version_file.write(version_number)

if not re.match(r"^([0-9]+)\.([0-9]+)\.([0-9]+)\.([0-9]+)$", version_number):
    logging.error("The version number needs to be in the form of four period-separated numbers: 0.0.0.0, %s is invalid", version_number)
    exit(-1)


setuptools.setup(
    name="ti-simplelink-crc-tool",

    # one-line description or tagline of what the project does.
    description='Tool to insert CRCs into ELF files or generate user records for CC23xx and CC27xx devices',

    # This is an optional longer description of your project that represents
    # the body of text which users will see when they visit PyPI.
    long_description=long_description,
    long_description_content_type='text/markdown',
    version=version_number,
    author="Texas Instruments",
    author_email="i.hovind@ti.com",
    license_files=("LICENSE.txt",),
    data_files=("version_number.txt",),
    packages=setuptools.find_packages(),
    package_data={
        "crc_tool": ["py.typed"],
    },
    entry_points={
        "console_scripts": [
            "crc_tool = crc_tool.main:app",
        ]
    },
    install_requires=[
        # DEPENDENCIES LAST UPDATED AT:
        # 2024-02-09, Ingebrigt Hovind
        # Key dependencies, install latest minor version
        "lief == 0.12.3",
        # Development dependencies
        # Using 6.4.0 caused it to be flagged as a virus by symantec
        # Downgrading to this (arbitrarily chosen) value fixed it
        "pyinstaller == 5.6.2",
        "cffi == 1.15.1",
        "pywin32-ctypes",
        "mypy",
        "pylint",
        "pytest",
    ],
)
