#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2023, Oracle and/or its affiliates.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License, version 2.0, as
# published by the Free Software Foundation.
#
# This program is also distributed with certain software (including
# but not limited to OpenSSL) that is licensed under separate terms,
# as designated in a particular file or component or in included license
# documentation.  The authors of MySQL hereby grant you an
# additional permission to link the program and your derivative works
# with the separately licensed software that they have included with
# MySQL.
#
# Without limiting anything contained in the foregoing, this file,
# which is part of MySQL Connector/Python, is also subject to the
# Universal FOSS Exception, version 1.0, a copy of which can be found at
# http://oss.oracle.com/licenses/universal-foss-exception.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License, version 2.0, for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin St, Fifth Floor, Boston, MA 02110-1301  USA

import os
import pathlib
import shutil
import sys

sys.path.insert(0, ".")

from cpydist import BuildExt, Install, InstallLib
from cpydist.bdist import DistBinary
from cpydist.bdist_solaris import DistSolaris
from cpydist.sdist import DistSource
from setuptools import Extension, find_packages, setup

try:
    from cpydist.bdist_wheel import DistWheel
except ImportError:
    DistWheel = None


METADATA_FILES = (
    "README.txt",
    "README.rst",
    "LICENSE.txt",
    "CHANGES.txt",
    "CONTRIBUTING.rst",
)


VERSION_TEXT = "999.0.0"
version_py = os.path.join("lib", "mysqlx", "version.py")
with open(version_py, "rb") as fp:
    exec(compile(fp.read(), version_py, "exec"))

COMMAND_CLASSES = {
    "bdist": DistBinary,
    "bdist_solaris": DistSolaris,
    "build_ext": BuildExt,
    "install": Install,
    "install_lib": InstallLib,
    "sdist": DistSource,
}

if DistWheel is not None:
    COMMAND_CLASSES["bdist_wheel"] = DistWheel

# C extensions
EXTENSIONS = [
    Extension(
        name="_mysqlxpb",
        define_macros=[("PY3", 1)] if sys.version_info[0] == 3 else [],
        sources=[
            "src/mysqlxpb/mysqlx/mysqlx.pb.cc",
            "src/mysqlxpb/mysqlx/mysqlx_connection.pb.cc",
            "src/mysqlxpb/mysqlx/mysqlx_crud.pb.cc",
            "src/mysqlxpb/mysqlx/mysqlx_cursor.pb.cc",
            "src/mysqlxpb/mysqlx/mysqlx_datatypes.pb.cc",
            "src/mysqlxpb/mysqlx/mysqlx_expect.pb.cc",
            "src/mysqlxpb/mysqlx/mysqlx_expr.pb.cc",
            "src/mysqlxpb/mysqlx/mysqlx_notice.pb.cc",
            "src/mysqlxpb/mysqlx/mysqlx_prepare.pb.cc",
            "src/mysqlxpb/mysqlx/mysqlx_resultset.pb.cc",
            "src/mysqlxpb/mysqlx/mysqlx_session.pb.cc",
            "src/mysqlxpb/mysqlx/mysqlx_sql.pb.cc",
            "src/mysqlxpb/mysqlxpb.cc",
        ],
    ),
]

LONG_DESCRIPTION = """
MySQL driver written in Python which implements the X DevAPI,
an Application Programming Interface for working with the
MySQL Document Store.
"""


def main() -> None:
    setup(
        name="mysqlx-connector-python",
        version=VERSION_TEXT,
        description="XDevAPI MySQL driver written in Python",
        long_description=LONG_DESCRIPTION,
        author="Oracle and/or its affiliates",
        author_email="",
        license="GNU GPLv2 (with FOSS License Exception)",
        keywords="mysql db",
        url="http://dev.mysql.com/doc/connector-python/en/index.html",
        download_url="http://dev.mysql.com/downloads/connector/python/",
        package_dir={"": "lib"},
        packages=find_packages(where="lib"),
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Environment :: Other Environment",
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "Intended Audience :: Information Technology",
            "Intended Audience :: System Administrators",
            "License :: OSI Approved :: GNU General Public License (GPL)",
            "Operating System :: OS Independent",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
            "Topic :: Database",
            "Topic :: Software Development",
            "Topic :: Software Development :: Libraries :: Application Frameworks",
            "Topic :: Software Development :: Libraries :: Python Modules",
        ],
        ext_modules=EXTENSIONS,
        cmdclass=COMMAND_CLASSES,
        python_requires=">=3.8",
        install_requires=["protobuf>=4.21.1,<=4.21.12"],
        extras_require={
            "dns-srv": ["dnspython>=1.16.0,<2.7.0"],
            "compression": ["lz4>=2.1.6,<=4.3.2", "zstandard>=0.12.0,<=0.19.0"],
        },
    )


def copy_metadata_files() -> None:
    """Copy metadata files (required by MANIFEST.in) from the
    parent directory to the current directory.
    """
    for filename in METADATA_FILES:
        shutil.copy(pathlib.Path(os.getcwd(), f"../{filename}"), pathlib.Path(f"./"))


def remove_metadata_files() -> None:
    """Remove files copied by `copy_metadata_files()`"""
    for filename in METADATA_FILES:
        os.remove(pathlib.Path(f"./{filename}"))


if __name__ == "__main__":
    copy_metadata_files()

    try:
        main()
    except Exception as err:
        raise err
    finally:
        remove_metadata_files()
