"""
    Tác giả: GnU
    Ngày tạo: 10/30/2023
    ©2023 LuaNonTeam
"""

import os
from os.path import join, abspath, dirname

from setuptools import setup, find_packages


def list_files(directory, excluded_folders):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        directories[:] = [d for d in directories if d not in excluded_folders]
        for filename in filenames:
            paths.append(os.path.join("..", path, filename))
    return paths


setup(
    name="luanon",
    version="1.0.1-dev",
    author="GnU",
    author_email="luanon404@gmail.com",
    description="Simple but gold",
    long_description=open(join(abspath(dirname(__file__)), "README.md"), encoding="UTF-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/luanon404/luanon",
    packages=find_packages(exclude=["venv", ".git"]),
    package_data={
        "": list_files("luanon", ["venv", ".git", "__pycache__"])
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    python_requires=">=3.12",
    install_requires=[],
    zipsafe=False
)