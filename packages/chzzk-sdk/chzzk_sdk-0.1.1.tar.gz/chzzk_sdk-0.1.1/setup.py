import re

import setuptools


version = None
with open("chzzk/__init__.py") as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE
    ).group(1)

if version is None:
    raise RuntimeError("version is not set")


setuptools.setup(
    name="chzzk-sdk",
    version=version,
    author="westreed",
    author_email="westreed@naver.com",
    description="An unofficial Python SDK Library for CHZZK",
    long_description_content_type="text/markdown",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    url="https://github.com/westreed/chzzk-sdk",
    install_requires=open("requirements.txt", "r", encoding="utf-8").read().splitlines(),
    packages=setuptools.find_packages(include=["chzzk", "chzzk.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11.7",
)
