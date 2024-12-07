.. _spkg_sagemath_brial:

===================================================================================
sagemath_brial: Boolean Ring Algebra with BRiAl
===================================================================================

About SageMath
--------------

   "Creating a Viable Open Source Alternative to
    Magma, Maple, Mathematica, and MATLAB"

   Copyright (C) 2005-2023 The Sage Development Team

   https://www.sagemath.org

SageMath fully supports all major Linux distributions, recent versions of
macOS, and Windows (using Cygwin or Windows Subsystem for Linux).

The traditional and recommended way to install SageMath is from source via
Sage-the-distribution (https://www.sagemath.org/download-source.html).
Sage-the-distribution first builds a large number of open source packages from
source (unless it finds suitable versions installed in the system) and then
installs the Sage Library (sagelib, implemented in Python and Cython).


About this pip-installable source distribution
----------------------------------------------

This pip-installable source distribution ``sagemath-brial`` provides
a Boolean Ring Algebra implementation using binary decision diagrams,
implemented by the BRiAl library, the successor to PolyBoRi.

Type
----

standard


Dependencies
------------

- $(PYTHON)
- $(PYTHON_TOOLCHAIN)
- :ref:`spkg_brial`
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

    passagemath-brial ~= 10.5.1.0


Equivalent System Packages
--------------------------

(none known)

