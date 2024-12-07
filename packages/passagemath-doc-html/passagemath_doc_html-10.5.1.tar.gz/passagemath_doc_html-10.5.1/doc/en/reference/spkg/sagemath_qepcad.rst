.. _spkg_sagemath_qepcad:

========================================================================================================
sagemath_qepcad: Quantifier elimination by partial cylindrical algebraic decomposition with QEPCAD
========================================================================================================

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

This pip-installable source distribution ``sagemath-qepcad`` provides an interface to QEPCAD.


Example
-------

::
   $ pipx run  --pip-args="--prefer-binary" --spec "passagemath-qepcad[test]" ipython

   In [1]: from sage.all__sagemath_symbolics import *

   In [2]: var('x,y')

   In [3]: ellipse = 3*x^2 + 2*x*y + y^2 - x + y - 7

   In [4]: F = qepcad_formula.exists(y, ellipse == 0); F

   In [5]: qepcad(F)

Type
----

optional


Dependencies
------------

- $(PYTHON)
- $(PYTHON_TOOLCHAIN)
- :ref:`spkg_cysignals`
- :ref:`spkg_cython`
- :ref:`spkg_pkgconfig`
- :ref:`spkg_qepcad`
- :ref:`spkg_sage_conf`
- :ref:`spkg_sage_setup`
- :ref:`spkg_sagemath_environment`
- :ref:`spkg_sagemath_repl`

Version Information
-------------------

package-version.txt::

    10.5.1

version_requirements.txt::

    passagemath-qepcad ~= 10.5.1.0


Equivalent System Packages
--------------------------

(none known)

