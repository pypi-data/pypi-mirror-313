.. _spkg_sagemath_libbraiding:

=======================================================================================
sagemath_libbraiding: Braid computations with libbraiding
=======================================================================================

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


About this pip-installable distribution
---------------------------------------

This pip-installable source distribution ``passagemath-libbraiding`` provides
an interface to `libbraiding <https://github.com/miguelmarco/libbraiding>`_,
a library to compute several properties of braids,
including centralizer and conjugacy check.


What is included
----------------

* `sage.libs.braiding <https://github.com/passagemath/passagemath/blob/main/src/sage/libs/braiding.pyx>`_


Examples
--------

::

    $ pipx run --pip-args="--prefer-binary" --spec "passagemath-libbraiding[test]" ipython

    In [1]: from sage.all__sagemath_libbraiding import *

    In [2]: from sage.libs.braiding import conjugatingbraid

    In [3]: B = BraidGroup(3); b = B([1,2,1,-2]); c = B([1,2])

    In [4]: conjugatingbraid(b,c)
    Out[4]: [[0], [2]]


Development
-----------

::

    $ git clone --origin passagemath https://github.com/passagemath/passagemath.git
    $ cd passagemath
    passagemath $ ./bootstrap
    passagemath $ python3 -m venv libbraiding-venv
    passagemath $ source libbraiding-venv/bin/activate
    (libbraiding-venv) passagemath $ pip install -v -e pkgs/sagemath-libbraiding

Type
----

standard


Dependencies
------------

- $(PYTHON)
- $(PYTHON_TOOLCHAIN)
- :ref:`spkg_cypari`
- :ref:`spkg_cython`
- :ref:`spkg_iml`
- :ref:`spkg_linbox`
- :ref:`spkg_m4ri`
- :ref:`spkg_m4rie`
- :ref:`spkg_memory_allocator`
- :ref:`spkg_pkgconfig`
- :ref:`spkg_sage_setup`
- :ref:`spkg_sagemath_categories`
- :ref:`spkg_sagemath_environment`
- :ref:`spkg_sagemath_flint`
- :ref:`spkg_sagemath_modules`

Version Information
-------------------

package-version.txt::

    10.5.1

version_requirements.txt::

    passagemath-libbraiding ~= 10.5.1.0


Equivalent System Packages
--------------------------

(none known)

