import codecs
import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()


def read(rel_path):
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


VERSION = get_version("layernext/__init__.py")
DESCRIPTION = "LayerNext Python SDK"
LONG_DESCRIPTION = "Python API Client to interact with LayerNext stack"

# Setting up
setup(
    name="layernext-beta",
    version=VERSION,
    author="LayerNext",
    author_email="<support@layernext.ai>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(
        include=[
            "layernext",
            "layernext.datalake",
            "layernext.dataset",
            "layernext.studio",
            "layernext.automatic_analysis",
        ]
    ),
    install_requires=[
        "requests",
        "uuid",
        "python-dotenv",
        "azure-storage-blob",
        "tqdm",
        "PyYAML",
        "Deprecated",
        "pymongo",
    ],
    keywords=[
        "python",
        "datalake",
        "datasetsync",
        "ai",
        "annotation",
        "layernext",
        "layernext",
        "machine learning",
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
