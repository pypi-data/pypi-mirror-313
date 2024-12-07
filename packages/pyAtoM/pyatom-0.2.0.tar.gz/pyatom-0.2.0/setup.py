import pathlib
import sys
import os
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

PKG = "pyAtoM"

# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()


# This call to setup() does all the work
setup(
    name=PKG,
    version="0.2.0",
    description="Python library for the AtoM archival description and access platform API",
    long_description=README,
    long_description_content_type="text/markdown",
    url="",
    author="James Carr",
    author_email="drjamescarr@gmail.com",
    license="Apache License 2.0",
    packages=["pyAtoM"],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: System :: Archiving",
    ],
    keywords='API Preservation',
    install_requires=["requests", "urllib3", "certifi"],
    project_urls={
        'Documentation': 'https://github.com/carj/pyAtoM',
        'Source': 'https://github.com/carj/pyAtoM',
        'Discussion Forum': 'https://github.com/carj/pyAtoM',
    }
)
