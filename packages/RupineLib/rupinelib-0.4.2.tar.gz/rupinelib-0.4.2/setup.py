import codecs
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.4.2'
DESCRIPTION = 'RupineLib'
LONG_DESCRIPTION = 'Rupine Python Library'

# Setting up
setup(
    name="RupineLib",
    version=VERSION,
    author="RupineLabs",
    author_email="<abc@def.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(where=here),
    install_requires=['psycopg2','pgcopy'],
    include_package_data=True,
    keywords=['web3'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)