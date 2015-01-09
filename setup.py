# -*- coding: utf-8 -*-


"""setup.py: setuptools control."""


import re
from setuptools import setup


version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('sqldevtodbext/sqldevtodbext.py').read(),
    re.M
    ).group(1)


with open("README.rst", "rb") as f:
    long_descr = f.read().decode("utf-8")


setup(
    name = "cmdline-sqldevtodbext",
    packages = ["sqldevtodbext"],
    entry_points = {
        "console_scripts": ['sqldevtodbext = sqldevtodbext.sqldevtodbext:main']
        },
    install_requires = [
        "argh",
        "argcomplete",
    ],
    version = version,
    description = "Export an Oracle SQL Developer profile to Vim DbExt",
    long_description = long_descr,
    author = "Nithin Philips",
    author_email = "nithin@nithinphilips.com",
    url = "",
    )
