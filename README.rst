=====================================================================================
 How to build and distribute a C++ shared library inside a Python wheel using Poetry
=====================================================================================

*The audience for this package is experienced Python developers who know how to build C and C++ extension modules. Knowledge of Cython is also assumed.*

This package shows how to build and distribute a C++ shared library inside a Python wheel using poetry_.

The most important pieces of the ``poetry_install_shared_lib_demo`` package are:

- ``build.py``
- ``poetry_install_shared_lib_demo/wrappers.pyx``: Cython file making use of the ``libprotobuf`` shared library.  ``build.py`` arranges for this file and the library to be compiled.
- ``pyproject.toml``: Contains the line ``build = build.py``

A more detailed discussion of how everything works follows the "Getting Started" section.

.. _poetry: https://python-poetry.org/

Getting Started
===============

::

    # first build the library and `make install` it in the package source directory
    PROTOBUF_SRC_URL=https://github.com/protocolbuffers/protobuf/releases/download/v3.11.3/protobuf-cpp-3.11.3.tar.gz
    curl -L "$PROTOBUF_SRC_URL" | tar -zxf -
    cd protobuf-3.11.3
    # install {include, lib} into `poetry_install_shared_lib_demo` source directory
    CXXFLAGS="-fPIC -g -std=c++11 -DNDEBUG" ./configure --prefix=$(pwd)/../poetry_install_shared_lib_demo
    make
    make install
    cd ..

    # build the package
    python3 -m pip install poetry
    python3 -m poetry build  # will fail, this is OK. See Note 1.
    python3 -m poetry run pip install Cython
    python3 -m poetry build

That's it. The wheel should be in the ``dist`` directory.

Notes
-----

1. Cython is a build requirement. It must be installed in the virtualenv poetry sets up for building the package. (The first ``poetry build`` creates this virtualenv.) Cython is neither a dependency nor a development dependency (using Poetry's terms). There does not appear to be a way to tell poetry about these kinds of dependencies. If anyone knows how to do this, please open an issue.
