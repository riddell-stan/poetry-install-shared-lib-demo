=====================================================================================
 How to build and distribute a C++ shared library inside a Python wheel using Poetry
=====================================================================================

*The target audience for this package is experienced Python developers who are familiar with building C and C++ extensions.*

This package shows how to build and distribute a C++ shared library inside a Python wheel using Poetry.

These instructions assume you are using Debian or Ubuntu Linux. They also assume you have write access to ``/usr/local/lib`` and ``/usr/local/bin``.

Getting Started
===============

    poetry build
    auditwheel repair dist/poetry_install_shared_lib_demo-0.1.0-cp37-cp37m-linux_x86_64.whl

The resulting wheel should be usable.
