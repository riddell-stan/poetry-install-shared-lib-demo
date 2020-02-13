=====================================================================================
 How to build and distribute a C++ shared library inside a Python wheel using Poetry
=====================================================================================

*The audience for this package is experienced Python developers who know how to build C and C++ extension modules. Knowledge of Cython is also assumed.*

This package shows how to build and distribute a C++ shared library inside a Python wheel using poetry_ and auditwheel_.
The wheel created using these instructions conforms to the manylinux2014_ standard and should be usable on most Linux systems.
This README also includes notes which may be of interest to developers seeking to understand how the ``auditwheel repair`` command works.

The most important pieces of the ``poetry_install_shared_lib_demo`` package are:

- ``build.py``
- ``poetry_install_shared_lib_demo/wrappers.pyx``: Cython file making use of the ``libprotobuf`` shared library.  ``build.py`` arranges for this file and the library to be compiled.
- ``pyproject.toml``: Contains the line ``build = build.py``

A more detailed discussion of how everything works follows the "Getting Started" section.

.. _poetry: https://python-poetry.org/
.. _auditwheel: https://github.com/pypa/auditwheel/
.. _manylinux2014: https://www.python.org/dev/peps/pep-0599/

Requirements
============

- docker (so we can use PyPA's ``manylinux2014`` build image)

Getting Started
===============

Here's an illustration of how this works. After cloning this repository,
issue the following command, which will place you into a bash shell inside the
manylinux2014 image::

    docker run -i -t -v `pwd`:/io quay.io/pypa/manylinux2014_x86_64 /bin/bash

Now run the following commands::

    cd /io
    python3 -m pip install poetry
    poetry build --format=wheel  # will fail, this is OK. See Note 1.
    poetry run pip install Cython
    poetry build --format=wheel
    auditwheel repair dist/poetry_install_shared_lib_demo-0.1.0-cp37-cp37m-linux_x86_64.whl

That's it. You should have a working, ``manylinux2014`` compliant wheel in
``wheelhouse``. This wheel contains a copy of the ``libprotobuf`` shared
library.

Notes
-----

1. Cython is a build requirement. It must be installed in the virtualenv poetry sets up for building the package. (The first ``poetry build`` creates this virtualenv.) Cython is neither a dependency nor a development dependency (using Poetry's terms). There does not appear to be a way to tell poetry about these kinds of dependencies. If anyone knows how to do this, please open an issue.

Notes on the actions ``auditwheel repair`` performs
===================================================

The following output should resemble the output you see when you run ``auditwheel repair``::

    [root@587539233e59 io]# auditwheel repair dist/poetry_install_shared_lib_demo-0.1.0-cp38-cp38-linux_x86_64.whl
    INFO:auditwheel.main_repair:Repairing poetry_install_shared_lib_demo-0.1.0-cp38-cp38-linux_x86_64.whl
    INFO:auditwheel.wheeltools:Previous filename tags: linux_x86_64
    INFO:auditwheel.wheeltools:New filename tags: manylinux2014_x86_64
    INFO:auditwheel.wheeltools:Previous WHEEL info tags: cp38-cp38-linux_x86_64
    INFO:auditwheel.wheeltools:New WHEEL info tags: cp38-cp38-manylinux2014_x86_64
    INFO:auditwheel.main_repair:
    Fixed-up wheel written to /io/wheelhouse/poetry_install_shared_lib_demo-0.1.0-cp38-cp38-manylinux2014_x86_64.whl

Let's examine the contents of the original wheel and the new wheel created by ``auditwheel repair``. Here are the files in the original::

    [root@587539233e59 io]# unzip -l dist/poetry_install_shared_lib_demo-0.1.0-cp38-cp38-linux_x86_64.whl
    Archive:  dist/poetry_install_shared_lib_demo-0.1.0-cp38-cp38-linux_x86_64.whl
      Length      Date    Time    Name
    ---------  ---------- -----   ----
           22  01-01-1980 00:00   poetry_install_shared_lib_demo/__init__.py
          588  01-01-1980 00:00   poetry_install_shared_lib_demo/wrappers.pyx
       523280  01-01-1980 00:00   poetry_install_shared_lib_demo/wrappers.cpython-38-x86_64-linux-gnu.so
       116867  01-01-1980 00:00   poetry_install_shared_lib_demo/wrappers.cpp
           94  01-01-2016 00:00   poetry_install_shared_lib_demo-0.1.0.dist-info/WHEEL
          406  01-01-2016 00:00   poetry_install_shared_lib_demo-0.1.0.dist-info/METADATA
          701  01-01-2016 00:00   poetry_install_shared_lib_demo-0.1.0.dist-info/RECORD
    ---------                     -------
       641958                     7 files


Note that there is no file with a name containing ``libprotobuf``.

Now let's look at the new version::

    [root@587539233e59 io]# unzip -l wheelhouse/poetry_install_shared_lib_demo-0.1.0-cp38-cp38-manylinux2014_x86_64.whl
    Archive:  wheelhouse/poetry_install_shared_lib_demo-0.1.0-cp38-cp38-manylinux2014_x86_64.whl
      Length      Date    Time    Name
    ---------  ---------- -----   ----
          838  02-11-2020 21:22   poetry_install_shared_lib_demo-0.1.0.dist-info/RECORD
          406  01-01-2016 00:00   poetry_install_shared_lib_demo-0.1.0.dist-info/METADATA
          103  02-11-2020 21:22   poetry_install_shared_lib_demo-0.1.0.dist-info/WHEEL
           22  01-01-1980 00:00   poetry_install_shared_lib_demo/__init__.py
          588  01-01-1980 00:00   poetry_install_shared_lib_demo/wrappers.pyx
       530976  02-11-2020 21:22   poetry_install_shared_lib_demo/wrappers.cpython-38-x86_64-linux-gnu.so
       116867  01-01-1980 00:00   poetry_install_shared_lib_demo/wrappers.cpp
     37549720  02-11-2020 21:22   poetry_install_shared_lib_demo/.libs/libprotobuf-3884000d.so.22.0.3
    ---------                     -------
     38199520                     8 files

The new version is much bigger (36.4 MiB vs. 0.6 MiB). The presence of the
``libprotobuf`` shared library is the primary reason for this. You can also see
that the file size of ``wrappers.cpython-38-x86_64-linux-gnu.so`` has changed
due to its having been patched.


FAQ
===

- What if I cannot or do not want to use ``auditwheel repair``?

There's almost no reason you would ever find yourself in such a situation. A
separate branch in this repository covers the changes required if you need to
perform some of the actions of ``auditwheel repair`` without using
``auditwheel``.
