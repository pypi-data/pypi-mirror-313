.. _spkg_sagemath_repl:

=============================================================================================
sagemath_repl: IPython kernel, Sage preparser, doctester
=============================================================================================

About SageMath
--------------

   "Creating a Viable Open Source Alternative to
    Magma, Maple, Mathematica, and MATLAB"

   Copyright (C) 2005-2024 The Sage Development Team

   https://www.sagemath.org

SageMath fully supports all major Linux distributions, recent versions of
macOS, and Windows (Windows Subsystem for Linux).

See https://doc.sagemath.org/html/en/installation/index.html
for general installation instructions.


About this pip-installable distribution package
-----------------------------------------------

The pip-installable source distribution `sagemath-repl` is a
distribution of a small part of the Sage Library.

It provides a small, fundamental subset of the modules of the Sage library
("sagelib", `sagemath-standard`), providing the IPython kernel, Sage preparser,
and doctester.


What is included
----------------

* `Doctesting Framework <https://doc.sagemath.org/html/en/reference/doctest/index.html>`_

* `The Sage REPL <https://doc.sagemath.org/html/en/reference/repl/sage/repl/index.html>`_

Type
----

standard


Dependencies
------------

- $(PYTHON)
- $(PYTHON_TOOLCHAIN)
- :ref:`spkg_ipython`
- :ref:`spkg_ipywidgets`
- :ref:`spkg_python_build`
- :ref:`spkg_sagemath_environment`
- :ref:`spkg_sagemath_objects`

Version Information
-------------------

package-version.txt::

    10.5.1

version_requirements.txt::

    passagemath-repl ~= 10.5.1.0


Equivalent System Packages
--------------------------

(none known)

