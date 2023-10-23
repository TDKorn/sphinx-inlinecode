import os
from setuptools import setup, find_packages

LONG_DESCRIPTION_SRC = 'README.rst'


def read(file):
    with open(os.path.abspath(file), 'r', encoding='utf-8') as f:
        return f.read()


def get_version():
    file = os.path.abspath(os.path.join('sphinx_inlinecode', '__init__.py'))
    for line in read(file).split('\n'):
        if line.startswith("__version__ ="):
            return line.split(" = ")[-1].strip('"')


setup(
    name="sphinx-inlinecode",
    version=get_version(),
    description="A Sphinx extension to embed source code blocks directly into documentation",
    long_description=read(LONG_DESCRIPTION_SRC),
    long_description_content_type="text/x-rst; charset=UTF-8",
    author="Adam Korn",
    author_email='hello@dailykitten.net',
    license="MIT License",
    packages=find_packages(exclude=("tests", "tests.*")),
    keywords=[
        "sphinx", "viewcode", "sphinx-extension", "sphinx-contrib", "code-block", "inline-code",
        "sphinx-ext", "inline", "embed", "documentation"
    ],
    url="https://github.com/tdkorn/sphinx-inlinecode",
    download_url="https://github.com/TDKorn/sphinx-inlinecode/tarball/main",
    package_data={
        "sphinx_inlinecode": [
            "_static/sphinx-inlinecode.css",
        ],
    },
    classifiers=[
        "Framework :: Sphinx :: Extension",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    install_requires=["sphinx>=1.8"],
)