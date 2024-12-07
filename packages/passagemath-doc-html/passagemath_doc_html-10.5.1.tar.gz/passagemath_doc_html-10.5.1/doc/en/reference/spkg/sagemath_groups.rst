.. _spkg_sagemath_groups:

===============================================================================
sagemath_groups: Groups and Invariant Theory
===============================================================================

About SageMath
--------------

   "Creating a Viable Open Source Alternative to
    Magma, Maple, Mathematica, and MATLAB"

   Copyright (C) 2005-2023 The Sage Development Team

   https://www.sagemath.org

SageMath fully supports all major Linux distributions, recent versions of macOS, and Windows (using Cygwin or Windows Subsystem for Linux).

The traditional and recommended way to install SageMath is from source via Sage-the-distribution (https://www.sagemath.org/download-source.html).  Sage-the-distribution first builds a large number of open source packages from source (unless it finds suitable versions installed in the system) and then installs the Sage Library (sagelib, implemented in Python and Cython).


About this experimental pip-installable source distribution
-----------------------------------------------------------

This pip-installable source distribution `sagemath-groups` is an experimental distribution of a part of the Sage Library.  Use at your own risk.  It provides a small subset of the modules of the Sage library ("sagelib", `sagemath-standard`).


What is included
----------------

* `Groups <https://doc.sagemath.org/html/en/reference/groups/index.html>`_

Type
----

standard


Dependencies
------------

- $(PYTHON)
- $(PYTHON_TOOLCHAIN)
- :ref:`spkg_cysignals`
- :ref:`spkg_cython`
- :ref:`spkg_gmpy2`
- :ref:`spkg_pkgconfig`
- :ref:`spkg_python_build`
- :ref:`spkg_sage_setup`
- :ref:`spkg_sagemath_environment`
- :ref:`spkg_sagemath_gap`
- :ref:`spkg_sagemath_linbox`
- :ref:`spkg_sagemath_modules`

Version Information
-------------------

package-version.txt::

    10.5.1

version_requirements.txt::

    passagemath-groups ~= 10.5.1.0


Equivalent System Packages
--------------------------

(none known)

